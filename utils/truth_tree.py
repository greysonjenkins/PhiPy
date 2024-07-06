# utils/truth_tree.py
from utils.logic import Formula, Atom, Not, And, Or, Implies
from typing import List
import graphviz

class TreeNode:
    def __init__(self, formula: Formula, closed=False):
        self.formula = formula
        self.closed = closed
        self.children = []

    def add_child(self, child: 'TreeNode'):
        self.children.append(child)

    def __repr__(self):
        return f"{formula_to_str(self.formula)}{' [x]' if self.closed else ''}"

class TruthTree:
    def __init__(self, root: TreeNode):
        self.root = root

def combine_premises(premises: List[Formula]) -> Formula:
    if not premises:
        raise ValueError("No premises provided")
    combined = premises[0]
    for premise in premises[1:]:
        combined = And(combined, premise)
    return combined

def generate_truth_tree(premises: List[Formula], conclusion: Formula) -> TruthTree:
    combined_premises = combine_premises(premises)
    root_formula = And(combined_premises, Not(conclusion))
    root = TreeNode(root_formula)
    truth_tree = TruthTree(root)
    expand_tree(root)
    return truth_tree

def expand_tree(node: TreeNode):
    if isinstance(node.formula, And):
        left_child = TreeNode(node.formula.left)
        right_child = TreeNode(node.formula.right)
        node.add_child(left_child)
        node.add_child(right_child)
        expand_tree(left_child)
        expand_tree(right_child)
    elif isinstance(node.formula, Or):
        left_child = TreeNode(node.formula.left)
        right_child = TreeNode(node.formula.right)
        node.add_child(left_child)
        node.add_child(right_child)
        expand_tree(left_child)
        expand_tree(right_child)
    elif isinstance(node.formula, Not):
        if isinstance(node.formula.formula, And):
            neg_left = TreeNode(Not(node.formula.formula.left))
            neg_right = TreeNode(Not(node.formula.formula.right))
            or_node = TreeNode(Or(neg_left.formula, neg_right.formula))
            node.add_child(or_node)
            expand_tree(or_node)
        elif isinstance(node.formula.formula, Or):
            neg_left = TreeNode(Not(node.formula.formula.left))
            neg_right = TreeNode(Not(node.formula.formula.right))
            and_node = TreeNode(And(neg_left.formula, neg_right.formula))
            node.add_child(and_node)
            expand_tree(and_node)
        elif isinstance(node.formula.formula, Not):
            actual_node = TreeNode(node.formula.formula.formula)
            node.add_child(actual_node)
            expand_tree(actual_node)
        else:
            actual_node = TreeNode(node.formula.formula)
            node.add_child(actual_node)
            expand_tree(actual_node)
    elif isinstance(node.formula, Implies):
        neg_left = TreeNode(Not(node.formula.left))
        or_node = TreeNode(Or(neg_left.formula, node.formula.right))
        node.add_child(or_node)
        expand_tree(or_node)
    else:
        pass

    mark_contradictions(node)

def mark_contradictions(node: TreeNode):
    formulas = set()
    check_for_contradictions(node, formulas)

def check_for_contradictions(node: TreeNode, formulas: set):
    if isinstance(node.formula, Not):
        if node.formula.formula in formulas:
            node.closed = True
    else:
        if Not(node.formula) in formulas:
            node.closed = True

    formulas.add(node.formula)

    for child in node.children:
        check_for_contradictions(child, formulas.copy())

def formula_to_str(formula: Formula) -> str:
    if isinstance(formula, Atom):
        return formula.name
    elif isinstance(formula, Not):
        return f"¬{formula_to_str(formula.formula)}"
    elif isinstance(formula, And):
        return f"({formula_to_str(formula.left)} ∧ {formula_to_str(formula.right)})"
    elif isinstance(formula, Or):
        return f"({formula_to_str(formula.left)} ∨ {formula_to_str(formula.right)})"
    elif isinstance(formula, Implies):
        return f"({formula_to_str(formula.left)} → {formula_to_str(formula.right)})"
    else:
        raise ValueError("Unknown formula type")

def print_truth_tree_graphviz(node: TreeNode, graph=None, parent_id=None) -> graphviz.Digraph:
    if graph is None:
        graph = graphviz.Digraph()

    node_id = str(id(node))
    label = formula_to_str(node.formula) + (' [x]' if node.closed else '')
    graph.node(node_id, label)

    if parent_id is not None:
        graph.edge(parent_id, node_id)

    for child in node.children:
        print_truth_tree_graphviz(child, graph, node_id)

    return graph

def check_validity(truth_tree: TruthTree):
    open_branches = []
    collect_open_branches(truth_tree.root, [], open_branches)

    if not open_branches:
        return True, None
    else:
        counterexample = {formula_to_str(node.formula): True for branch in open_branches for node in branch}
        return False, counterexample

def collect_open_branches(node: TreeNode, current_branch, open_branches):
    current_branch.append(node)
    if not node.children and not node.closed:
        open_branches.append(current_branch)
    else:
        for child in node.children:
            collect_open_branches(child, current_branch[:], open_branches)