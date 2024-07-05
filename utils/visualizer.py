import graphviz
from utils.logic import Formula, Atom, Not, And, Or, Implies

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

def visualize_tree(root):
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')

    def add_node(node, parent_id=None):
        node_id = str(id(node))
        dot.node(node_id, formula_to_str(node.formula))
        if parent_id:
            dot.edge(parent_id, node_id)
        for child in node.children:
            add_node(child, node_id)

    add_node(root)
    return dot