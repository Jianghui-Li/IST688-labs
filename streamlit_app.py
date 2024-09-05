import streamlit as st

# Set up the main configuration for the app
st.set_page_config(page_title="My App", layout="centered")

# Create a sidebar for navigation between the pages
st.sidebar.title("Navigation")
st.sidebar.write("Select a page below:")

# List the pages as links in the sidebar
st.sidebar.markdown("[Go to Page 1](page1)")
st.sidebar.markdown("[Go to Page 2](page2)")

# Add some basic instructions or introductory text on the main page
st.title("Welcome to the Document Question Answering App")
st.write(
    """
    Use the sidebar to navigate between the pages:
    - **Page 1**: Upload a document and ask questions.
    - **Page 2**: Perform a different type of analysis or ask other questions.
    """
)
