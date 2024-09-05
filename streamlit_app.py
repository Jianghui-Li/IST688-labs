import streamlit as st

# Set up the main configuration for the app
st.set_page_config(page_title="Document Question Answering App", layout="centered")

# Title for the main page
st.title("Welcome to the Document Question Answering App")

# Introduction text
st.write(
    """
    Use the links below to navigate to the different labs:
    """
)

# Create clickable links for Lab 1 and Lab 2
st.markdown("[Go to Lab 1](Lab1)")
st.markdown("[Go to Lab 2](Lab2)")

# Add some description for each lab
st.write(
    """
    - **Lab 1**: Upload a document and ask questions using GPT.
    - **Lab 2**: Perform another type of analysis or ask additional questions.
    """
)
