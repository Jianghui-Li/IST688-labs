import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Lab Navigation App", layout="centered")

# Create navigation using a selectbox
page = st.selectbox("Choose a lab page", ("Lab 1", "Lab 2"))

# Display the selected lab page content
if page == "Lab 1":
    st.write("# Lab 1: Document Upload and Question Answering")
    # Include logic for Lab 1 (e.g., document upload, OpenAI API interaction)
    import pages.lab1  # Importing the lab1 page logic from another file
elif page == "Lab 2":
    st.write("# Lab 2: Another Type of Analysis")
    # Include logic for Lab 2 (e.g., other analysis or features)
    import pages.lab2  # Importing the lab2 page logic from another file
