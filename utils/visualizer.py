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
    else:
        raise ValueError("Unknown formula type")


def visualize_tree(truth_tree) -> str:
    dot = graphviz.Digraph(comment='Truth Tree')

    def add_node(node, parent=None):
        label = formula_to_str(node.formula)
        dot.node(str(id(node)), label)
        if parent:
            dot.edge(str(id(parent)), str(id(node)))
        for child in node.children:
            add_node(child, node)

    add_node(truth_tree.root)
    return dot.source