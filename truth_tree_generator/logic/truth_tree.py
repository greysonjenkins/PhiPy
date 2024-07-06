from .parser import TokenType, ASTNode


class TreeNode:
    def __init__(self, formula, parent=None, rule=None):
        self.formula = formula
        self.parent = parent
        self.children = []
        self.closed = False
        self.rule = rule

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


class TruthTree:
    def __init__(self, root):
        self.root = root

    def is_valid(self):
        return all(leaf.closed for leaf in self.get_leaves())

    def get_leaves(self):
        def collect_leaves(node):
            if not node.children:
                return [node]
            leaves = []
            for child in node.children:
                leaves.extend(collect_leaves(child))
            return leaves

        return collect_leaves(self.root)


def generate_truth_tree(sentences):
    root = TreeNode(None)
    for sentence in sentences:
        root.add_child(TreeNode(sentence))

    tree = TruthTree(root)
    expand_tree(tree)
    check_closure(tree)
    return tree


def expand_tree(tree):
    leaves = tree.get_leaves()
    while any(can_decompose(leaf) for leaf in leaves):
        for leaf in leaves:
            if can_decompose(leaf):
                decompose_node(leaf)
        leaves = tree.get_leaves()


def can_decompose(node):
    return node.formula.type != TokenType.ATOM


def decompose_node(node):
    formula_type = node.formula.type
    if formula_type == TokenType.AND:
        node.add_child(TreeNode(node.formula.left, rule="∧"))
        node.children[-1].add_child(TreeNode(node.formula.right, rule="∧"))
    elif formula_type == TokenType.OR:
        node.add_child(TreeNode(node.formula.left, rule="∨"))
        node.add_child(TreeNode(node.formula.right, rule="∨"))
    elif formula_type == TokenType.IMPLIES:
        node.add_child(TreeNode(ASTNode(TokenType.NOT, left=node.formula.left), rule="→"))
        node.add_child(TreeNode(node.formula.right, rule="→"))
    elif formula_type == TokenType.IFF:
        left_impl = ASTNode(TokenType.IMPLIES, left=node.formula.left, right=node.formula.right)
        right_impl = ASTNode(TokenType.IMPLIES, left=node.formula.right, right=node.formula.left)
        node.add_child(TreeNode(left_impl, rule="↔"))
        node.children[-1].add_child(TreeNode(right_impl, rule="↔"))
    elif formula_type == TokenType.NOT:
        if node.formula.left.type == TokenType.NOT:
            node.add_child(TreeNode(node.formula.left.left, rule="¬¬"))
        elif node.formula.left.type == TokenType.AND:
            node.add_child(TreeNode(ASTNode(TokenType.NOT, left=node.formula.left.left), rule="¬∧"))
            node.add_child(TreeNode(ASTNode(TokenType.NOT, left=node.formula.left.right), rule="¬∧"))
        elif node.formula.left.type == TokenType.OR:
            node.add_child(TreeNode(ASTNode(TokenType.NOT, left=node.formula.left.left), rule="¬∨"))
            node.children[-1].add_child(TreeNode(ASTNode(TokenType.NOT, left=node.formula.left.right), rule="¬∨"))
        elif node.formula.left.type == TokenType.IMPLIES:
            node.add_child(TreeNode(node.formula.left.left, rule="¬→"))
            node.children[-1].add_child(TreeNode(ASTNode(TokenType.NOT, left=node.formula.left.right), rule="¬→"))


def check_closure(tree):
    def collect_literals(node):
        if node.formula.type == TokenType.ATOM:
            return {node.formula.value}
        elif node.formula.type == TokenType.NOT and node.formula.left.type == TokenType.ATOM:
            return {f"¬{node.formula.left.value}"}
        return set()

    def check_node_closure(node):
        literals = set()
        current = node
        while current:
            literals.update(collect_literals(current))
            current = current.parent

        for literal in literals:
            if literal.startswith("¬"):
                if literal[1:] in literals:
                    return True
            else:
                if f"¬{literal}" in literals:
                    return True
        return False

    for leaf in tree.get_leaves():
        if check_node_closure(leaf):
            leaf.closed = True


# Helper function to convert AST back to string (for debugging)
def formula_to_string(node):
    if node.type == TokenType.ATOM:
        return node.value
    elif node.type == TokenType.NOT:
        return f"¬({formula_to_string(node.left)})"
    elif node.type in [TokenType.AND, TokenType.OR, TokenType.IMPLIES, TokenType.IFF]:
        op = {TokenType.AND: '∧', TokenType.OR: '∨', TokenType.IMPLIES: '→', TokenType.IFF: '↔'}[node.type]
        return f"({formula_to_string(node.left)} {op} {formula_to_string(node.right)})"