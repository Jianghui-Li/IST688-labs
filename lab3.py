import streamlit as st
from openai import OpenAI

st.title("My Lab3 question answering chatbot")

openAI_model = st.sidebar.selectbox("Which Model?",("mini","regular"))
if openAI_model == "mini":
    model_to_use = "gpt-4o-mini"
else:
    model_to_use = "gpt-4o"

if 'client' not in st.session_state:
    api_key = st.secrets["API_KEY"]
    st.session_state.client = OpenAI(api_key = api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = \
        [{"role": "assistant", "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    chat_msg = st.chat_message(msg["role"])
    chat_msg.write(msg["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = st.session_state.client
    stream = client.chat.completions.create(
        model = model_to_use,
        messages = st.session_state.messages,
        stream = True
    )
    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})