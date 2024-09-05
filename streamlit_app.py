import streamlit as st

st.set_page_config(page_title="Lab Navigation App", layout="centered")

page = st.selectbox("Choose a lab page", ("Lab 1", "Lab 2"))

if page == "Lab 1":
    st.write("# Lab 1: Document Upload and Question Answering")
    import pages.lab1
elif page == "Lab 2":
    st.write("# Lab 2: Another Type of Analysis")
    import pages.lab2
