import streamlit as st
from openai import OpenAI

# Configure page settings
st.set_page_config(page_title="Document Question Answering App", layout="centered")

# Show title and description
st.title("Welcome to My Document Question Answering App")
st.write(
    "Upload a document and navigate to different pages to ask questions about it!"
    " To use this app, you need to provide an OpenAI API key."
)

# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

# The sidebar will contain the navigation to different pages.
st.sidebar.title("Navigation")
st.sidebar.write("Go to a page to upload a file and ask questions.")

