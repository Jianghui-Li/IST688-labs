import streamlit as st

lab1 = st.Page("lab1.py", title= "lab1")
lab2 = st.Page("lab2.py", title= "lab2")
lab3 = st.Page("lab3.py", title= "lab3")

pg = st.navigation([lab1, lab2, lab3])
st.set_page_config(page_title="Document", page_icon=":material/edit:")
pg.run()