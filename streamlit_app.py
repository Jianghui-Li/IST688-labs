import streamlit as st

st.set_page_config(page_title="My App", layout="centered")

st.sidebar.title("Labs")
st.sidebar.write("Select a page below:")

# List the pages as links in the sidebar
st.sidebar.markdown("[Go to Lab 1](lab1)")
st.sidebar.markdown("[Go to Lab 2](lab2)")

# Add some basic instructions or introductory text on the main page
st.title("Welcome to My App")
st.write(
    """
    Use the sidebar to navigate between the pages:
    - **Lab 1**: Upload a document and ask questions.
    - **Lab 2**: Lab2.
    """
)
