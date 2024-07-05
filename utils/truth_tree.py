from typing import List, Tuple, Dict
from utils.logic import Formula, Atom, Not, And, Or, Implies


class TreeNode:
    def __init__(self, formula: Formula):
        self.formula = formula
        self.children: List[TreeNode] = []
        self.closed = False
        self.parent = None


def expand_node(node: TreeNode):
    formula = node.formula
    if isinstance(formula, And):
        left_child = TreeNode(formula.left)
        right_child = TreeNode(formula.right)
        node.children = [left_child, right_child]
        left_child.parent = node
        right_child.parent = node
    elif isinstance(formula, Or):
        left_child = TreeNode(formula.left)
        right_child = TreeNode(formula.right)
        node.children = [left_child, right_child]
        left_child.parent = node
        right_child.parent = node
    elif isinstance(formula, Implies):
        left_child = TreeNode(Not(formula.left))
        right_child = TreeNode(formula.right)
        node.children = [left_child, right_child]
        left_child.parent = node
        right_child.parent = node
    elif isinstance(formula, Not):
        if isinstance(formula.formula, Not):
            child = TreeNode(formula.formula.formula)
            node.children = [child]
            child.parent = node
        elif isinstance(formula.formula, And):
            left_child = TreeNode(Not(formula.formula.left))
            right_child = TreeNode(Not(formula.formula.right))
            node.children = [left_child, right_child]
            left_child.parent = node
            right_child.parent = node
        elif isinstance(formula.formula, Or):
            child = TreeNode(And(Not(formula.formula.left), Not(formula.formula.right)))
            node.children = [child]
            child.parent = node
        elif isinstance(formula.formula, Implies):
            child = TreeNode(And(formula.formula.left, Not(formula.formula.right)))
            node.children = [child]
            child.parent = node


def generate_truth_tree(premises: List[Formula], conclusion: Formula) -> TreeNode:
    # Combine premises with the negation of the conclusion
    if len(premises) == 1:
        root_formula = And(premises[0], Not(conclusion))
    else:
        root_formula = premises[0]
        for premise in premises[1:]:
            root_formula = And(root_formula, premise)
        root_formula = And(root_formula, Not(conclusion))

    root = TreeNode(root_formula)
    stack = [root]

    while stack:
        node = stack.pop(0)  # Change to BFS
        expand_node(node)
        stack.extend(node.children)

    return root


def check_validity(tree: TreeNode) -> Tuple[bool, Union[Dict[str, bool], List[Formula]]]:
    def is_closed(node: TreeNode) -> bool:
        formulas = set()
        current = node
        while current:
            if isinstance(current.formula, Atom):
                if Not(current.formula) in formulas:
                    return True
                formulas.add(current.formula)
            elif isinstance(current.formula, Not) and isinstance(current.formula.formula, Atom):
                if current.formula.formula in formulas:
                    return True
                formulas.add(current.formula)
            elif isinstance(current.formula, And):
                formulas.add(current.formula.left)
                formulas.add(current.formula.right)
            current = current.parent
        return False

    def is_tree_closed(node: TreeNode) -> bool:
        if not node.children:
            return is_closed(node)
        return all(is_tree_closed(child) for child in node.children)

    def get_open_branch(node: TreeNode) -> List[Formula]:
        if not node.children:
            return [node.formula] if not is_closed(node) else []
        for child in node.children:
            branch = get_open_branch(child)
            if branch:
                return [node.formula] + branch
        return []

    def extract_atoms(formulas: List[Formula]) -> Dict[str, bool]:
        atoms = {}
        for formula in formulas:
            if isinstance(formula, Atom):
                atoms[formula.name] = True
            elif isinstance(formula, Not) and isinstance(formula.formula, Atom):
                atoms[formula.formula.name] = False
        return atoms

    is_valid = is_tree_closed(tree)
    counterexample = [] if is_valid else extract_atoms(get_open_branch(tree))
    return is_valid, counterexample