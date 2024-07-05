import streamlit as st

st.set_page_config(
    page_title="PhiPy",
    page_icon="φ")

st.write("Welcome to PhiPy on Streamlit!")

st.sidebar.success("Select a tool.")

st.markdown(
    """
    PhiPy is an open-source framework built specifically for
    analyzing philosophical arguments and computational linguistics.
    
    **👈 Select a tool from the sidebar** to see some examples
    of what PhiPy can do!
"""
)
