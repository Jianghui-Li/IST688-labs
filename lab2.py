import streamlit as st
import secrets
import string

st.title("Secret Key Generator (Lab 2)")

def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

length = st.slider("Select the length of the secret key", min_value=8, max_value=64, value=32)

if st.button("Generate Secret Key"):
    secret_key = generate_secret_key(length)
    st.write(f"Your generated secret key is: `{secret_key}`")
    st.code(secret_key, language="bash")
