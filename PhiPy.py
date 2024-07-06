# PhiPy.py
import streamlit as st
import sys
import os

# Ensure the root directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(
    page_title="PhiPy",
    page_icon="φ"
)

st.write("Welcome to PhiPy on Streamlit!")

# Navigation
tool = st.sidebar.selectbox("Select a Tool", ["Home", "Argument Analyzer"])

if tool == "Home":
    st.markdown(
        """
        PhiPy is an open-source framework built specifically for
        analyzing philosophical arguments and computational linguistics.

        **👈 Select a tool from the sidebar** to see some examples
        of what PhiPy can do!
        """
    )
elif tool == "Argument Analyzer":
    from pages.Argument_Analyzer import run

    run()