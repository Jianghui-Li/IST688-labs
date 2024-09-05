import streamlit as st

# Set up the main configuration for the app
st.set_page_config(page_title="Lab Navigation", layout="centered")

# Create a sidebar for navigation between the labs
st.sidebar.title("Lab Navigation")
selected_lab = st.sidebar.selectbox("Choose a Lab", ["Lab 1", "Lab 2"])

# Display the selected page based on navigation
if selected_lab == "Lab 1":
    st.write("You are on **Lab 1** page")
    # Importing Lab 1 as a function or code block
    import lab1
    lab1.display_lab1()
elif selected_lab == "Lab 2":
    st.write("You are on **Lab 2** page")
    # Importing Lab 2 as a function or code block
    import lab2
    lab2.display_lab2()
