from graphviz import Digraph
from .truth_tree import formula_to_string, generate_truth_tree
from .parser import TokenType, parse_sentences

def visualize_tree(tree, options):
    dot = Digraph(comment='Truth Tree')
    dot.attr(rankdir='TB')
    dot.attr('node', shape='plaintext')

    def add_node(node, parent_id=None):
        node_id = str(id(node))
        label = []

        if options.get('show_line_numbers', True):
            label.append(f"{node.line_number}. ")

        formula_str = formula_to_string(node.formula)
        if options.get('circle_atomic', False) and node.formula.type == TokenType.ATOM:
            formula_str = f"⊚{formula_str}⊚"
        label.append(formula_str)

        if node.closed:
            label.append(" ×")

        label = " ".join(label)

        if options.get('show_decomposition_rule', False) and node.rule:
            label += f" ({node.rule})"

        dot.node(node_id, label)

        if parent_id:
            dot.edge(parent_id, node_id)

        for child in node.children:
            add_node(child, node_id)

    # Add root's children (premises)
    for i, child in enumerate(tree.root.children):
        child.line_number = i + 1
        add_node(child)

    # Number the rest of the nodes
    def number_nodes(node, current_number):
        for child in node.children:
            current_number += 1
            child.line_number = current_number
            current_number = number_nodes(child, current_number)
        return current_number

    number_nodes(tree.root, len(tree.root.children))

    if options.get('mark_closed_branches', True):
        for leaf in tree.get_leaves():
            if leaf.closed:
                path = []
                current = leaf
                while current.parent:
                    path.append(str(id(current)))
                    current = current.parent
                for i in range(len(path) - 1):
                    dot.edge(path[i + 1], path[i], color='red', penwidth='2')

    return dot.source


# For debugging
if __name__ == "__main__":

    test_sentences = ["P → Q", "P", "¬Q"]
    parsed_sentences = parse_sentences(test_sentences)
    truth_tree = generate_truth_tree(parsed_sentences)
    options = {'show_line_numbers': True, 'circle_atomic': False, 'mark_closed_branches': True,
               'show_decomposition_rule': False}

    tree_graph = visualize_tree(truth_tree, options)
    print(tree_graph)