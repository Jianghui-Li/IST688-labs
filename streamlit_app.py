import streamlit as st

# Set up the main configuration for the app
st.set_page_config(page_title="Lab Navigation", layout="centered")

# Create a sidebar for navigation between the labs
st.sidebar.title("Lab Navigation")
selected_lab = st.sidebar.selectbox("Choose a Lab", ["Lab 1", "Lab 2"])

