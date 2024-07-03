import streamlit as st

st.set_page_config(
    page_title="PyPhi",
    page_icon="φ")

st.write("Welcome to PyPhi!")

st.sidebar.success("Select a tool above.")

st.markdown(
    """
    PyPhi is an open-source framework built specifically for
    analyzing philosophical arguments and computational linguistics.
    **👈 Select a tool from the sidebar** to see some examples
    of what PyPhi can do!
"""
)