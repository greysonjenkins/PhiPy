import streamlit as st
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.logic import Formula, Atom, Not, And, Or, Implies
from utils.parser import parse_argument
from utils.truth_tree import generate_truth_tree, check_validity
from utils.visualizer import visualize_tree

def run():
    st.title("Formal Argument Analyzer")

    premises = st.text_area("Enter premises (one per line):")
    conclusion = st.text_input("Enter conclusion:")

    if st.button("Analyze Argument"):
        try:
            # Parse the input
            parsed_premises = [parse_argument(premise) for premise in premises.split('\n') if premise.strip()]
            parsed_conclusion = parse_argument(conclusion)

            # Generate truth tree
            truth_tree = generate_truth_tree(parsed_premises, parsed_conclusion)

            # Check validity
            is_valid, counterexample = check_validity(truth_tree)

            # Visualize the tree
            tree_graph = visualize_tree(truth_tree)
            st.graphviz_chart(tree_graph)

            # Display results
            if is_valid:
                st.success("The argument is valid.")
            else:
                st.error("The argument is invalid.")
                st.write("Counterexample:", counterexample)

            # Add an explanation
            st.write("Explanation:")
            if is_valid:
                st.write("This argument is an application of modus tollens (denying the consequent). "
                         "It's a valid form of argument in propositional logic.")
            else:
                st.write("If the argument were valid, there would be no way to make all premises true "
                         "and the conclusion false. The counterexample shows a scenario where this happens.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run()
