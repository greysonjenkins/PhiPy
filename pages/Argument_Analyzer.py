# pages/Argument_Analyzer.py
import streamlit as st
from utils.parser import parse_argument
from utils.truth_tree import generate_truth_tree, check_validity, print_truth_tree_graphviz
import graphviz

def run():
    st.title("Argument Analyzer")

    premises = st.text_area("Enter premises (one per line):")
    conclusion = st.text_input("Enter conclusion:")

    if st.button("Analyze Argument"):
        try:
            parsed_premises = [parse_argument(premise) for premise in premises.split('\n') if premise.strip()]
            if not parsed_premises:
                st.error("Please enter at least one premise.")
                return
            parsed_conclusion = parse_argument(conclusion)
            if not conclusion.strip():
                st.error("Please enter a conclusion.")
                return

            st.write("Parsed Premises:")
            for premise in parsed_premises:
                st.write(str(premise))

            st.write("Parsed Conclusion:")
            st.write(str(parsed_conclusion))

            truth_tree = generate_truth_tree(parsed_premises, parsed_conclusion)
            st.markdown("<h3>Truth Tree:</h3>", unsafe_allow_html=True)
            graph = print_truth_tree_graphviz(truth_tree.root)
            st.graphviz_chart(graph.source)

            is_valid, counterexample = check_validity(truth_tree)

            if is_valid:
                st.success("The argument is valid.")
            else:
                st.error("The argument is invalid.")
                if counterexample:
                    st.write("Counterexample:", ", ".join(f"{k}: {v}" for k, v in counterexample.items()))
                else:
                    st.write("No specific counterexample found.")

            st.write("Explanation:")
            if is_valid:
                st.write("This argument is valid. The truth tree closes all branches, "
                         "indicating that there's no way to make all premises true "
                         "and the conclusion false simultaneously.")
            else:
                st.write("This argument is invalid. The truth tree has at least one open branch, "
                         "which represents a scenario where all premises are true "
                         "but the conclusion is false.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run()