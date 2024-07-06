from flask import Flask, render_template, request, jsonify
from enum import Enum
import graphviz


app = Flask(__name__)


class TokenType(Enum):
    ATOM = 1
    AND = 2
    OR = 3
    NOT = 4
    IMPLIES = 5
    IFF = 6


class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right


def parse_sentence(sentence):
    tokens = tokenize(sentence)
    return parse_expression(tokens)


def tokenize(sentence):
    tokens = []
    i = 0
    while i < len(sentence):
        if sentence[i].isalpha():
            tokens.append((TokenType.ATOM, sentence[i]))
        elif sentence[i] == '∧':
            tokens.append((TokenType.AND, '∧'))
        elif sentence[i] == '∨':
            tokens.append((TokenType.OR, '∨'))
        elif sentence[i] == '¬':
            tokens.append((TokenType.NOT, '¬'))
        elif sentence[i] == '→':
            tokens.append((TokenType.IMPLIES, '→'))
        elif sentence[i:i + 2] == '↔':
            tokens.append((TokenType.IFF, '↔'))
            i += 1
        elif sentence[i] in '()':
            tokens.append((None, sentence[i]))
        i += 1
    return tokens


def parse_expression(tokens):
    def parse_iff():
        left = parse_implies()
        while tokens and tokens[0][1] == '↔':
            tokens.pop(0)
            right = parse_implies()
            left = ASTNode(TokenType.IFF, left=left, right=right)
        return left

    def parse_implies():
        left = parse_or()
        while tokens and tokens[0][1] == '→':
            tokens.pop(0)
            right = parse_or()
            left = ASTNode(TokenType.IMPLIES, left=left, right=right)
        return left

    def parse_or():
        left = parse_and()
        while tokens and tokens[0][1] == '∨':
            tokens.pop(0)
            right = parse_and()
            left = ASTNode(TokenType.OR, left=left, right=right)
        return left

    def parse_and():
        left = parse_not()
        while tokens and tokens[0][1] == '∧':
            tokens.pop(0)
            right = parse_not()
            left = ASTNode(TokenType.AND, left=left, right=right)
        return left

    def parse_not():
        if tokens and tokens[0][1] == '¬':
            tokens.pop(0)
            return ASTNode(TokenType.NOT, left=parse_not())
        return parse_atom()

    def parse_atom():
        if tokens[0][1] == '(':
            tokens.pop(0)
            expr = parse_iff()
            if tokens[0][1] != ')':
                raise ValueError("Missing closing parenthesis")
            tokens.pop(0)
            return expr
        if tokens[0][0] == TokenType.ATOM:
            return ASTNode(TokenType.ATOM, value=tokens.pop(0)[1])
        raise ValueError(f"Unexpected token: {tokens[0][1]}")

    return parse_iff()


class TreeNode:
    def __init__(self, formula, parent=None):
        self.formula = formula
        self.parent = parent
        self.children = []
        self.closed = False


def generate_truth_tree(premises):
    root = TreeNode(None)  # Root node with no formula
    leaves = [root]

    def expand_node(node, formula):
        if formula.type == TokenType.AND:
            node.children.append(TreeNode(formula.left, node))
            node.children[-1].children.append(TreeNode(formula.right, node.children[-1]))
            return node.children[-1].children
        elif formula.type == TokenType.OR:
            node.children.append(TreeNode(formula.left, node))
            node.children.append(TreeNode(formula.right, node))
            return node.children
        elif formula.type == TokenType.IMPLIES:
            not_left = ASTNode(TokenType.NOT, left=formula.left)
            node.children.append(TreeNode(not_left, node))
            node.children.append(TreeNode(formula.right, node))
            return node.children
        elif formula.type == TokenType.IFF:
            left_implies_right = ASTNode(TokenType.IMPLIES, left=formula.left, right=formula.right)
            right_implies_left = ASTNode(TokenType.IMPLIES, left=formula.right, right=formula.left)
            node.children.append(TreeNode(left_implies_right, node))
            node.children.append(TreeNode(right_implies_left, node))
            return node.children
        elif formula.type == TokenType.NOT:
            if formula.left.type == TokenType.NOT:
                node.children.append(TreeNode(formula.left.left, node))
                return node.children
            elif formula.left.type == TokenType.AND:
                not_left = ASTNode(TokenType.NOT, left=formula.left.left)
                not_right = ASTNode(TokenType.NOT, left=formula.left.right)
                node.children.append(TreeNode(not_left, node))
                node.children.append(TreeNode(not_right, node))
                return node.children
            elif formula.left.type == TokenType.OR:
                not_left = ASTNode(TokenType.NOT, left=formula.left.left)
                not_right = ASTNode(TokenType.NOT, left=formula.left.right)
                node.children.append(TreeNode(not_left, node))
                node.children[-1].children.append(TreeNode(not_right, node.children[-1]))
                return node.children[-1].children
            elif formula.left.type == TokenType.IMPLIES:
                node.children.append(TreeNode(formula.left.left, node))
                not_right = ASTNode(TokenType.NOT, left=formula.left.right)
                node.children[-1].children.append(TreeNode(not_right, node.children[-1]))
                return node.children[-1].children
        return [TreeNode(formula, node)]

    def check_contradiction(node):
        formulas = []
        current = node
        while current:
            if current.formula:
                formulas.append(current.formula)
            current = current.parent

        for i, formula in enumerate(formulas):
            if formula.type == TokenType.ATOM:
                for other in formulas[i + 1:]:
                    if other.type == TokenType.NOT and other.left.type == TokenType.ATOM and other.left.value == formula.value:
                        return True
            elif formula.type == TokenType.NOT and formula.left.type == TokenType.ATOM:
                for other in formulas[i + 1:]:
                    if other.type == TokenType.ATOM and other.value == formula.left.value:
                        return True
        return False

    # Process premises
    for premise in premises:
        new_leaves = []
        for leaf in leaves:
            new_leaves.extend(expand_node(leaf, premise))
        leaves = new_leaves

    # Expand the tree
    while True:
        expanded = False
        new_leaves = []
        for leaf in leaves:
            if leaf.formula and leaf.formula.type != TokenType.ATOM and leaf.formula.type != TokenType.NOT:
                new_leaves.extend(expand_node(leaf, leaf.formula))
                expanded = True
            else:
                new_leaves.append(leaf)

        leaves = new_leaves
        if not expanded:
            break

    # Check for contradictions
    for leaf in leaves:
        if check_contradiction(leaf):
            leaf.closed = True

    return root


def visualize_tree(root):
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')

    def add_node(node, parent_id=None):
        node_id = str(id(node))
        label = formula_to_string(node.formula) if node.formula else "Root"
        if node.closed:
            label += " ×"
        dot.node(node_id, label)
        if parent_id:
            dot.edge(parent_id, node_id)
        for child in node.children:
            add_node(child, node_id)

    add_node(root)
    return dot


def formula_to_string(node):
    if node is None:
        return "Root"
    if node.type == TokenType.ATOM:
        return node.value
    elif node.type == TokenType.NOT:
        return f"¬({formula_to_string(node.left)})"
    elif node.type in [TokenType.AND, TokenType.OR, TokenType.IMPLIES, TokenType.IFF]:
        op = {TokenType.AND: '∧', TokenType.OR: '∨', TokenType.IMPLIES: '→', TokenType.IFF: '↔'}[node.type]
        return f"({formula_to_string(node.left)} {op} {formula_to_string(node.right)})"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_tree', methods=['POST'])
def generate_tree():
    data = request.json
    sentences = data.get('sentences', [])

    try:
        parsed_sentences = [parse_sentence(sentence) for sentence in sentences]
        truth_tree = generate_truth_tree(parsed_sentences)
        dot = visualize_tree(truth_tree)

        return jsonify({
            'tree': dot.source,
            'is_valid': all(leaf.closed for leaf in truth_tree.children)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)