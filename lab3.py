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

def limit_messages(messages, limit=2):
    user_msgs = [msg for msg in messages if msg["role"] == "user"]
    if len(user_msgs) > limit:
        user_msgs = user_msgs[-limit:]
    assistant_msgs = [msg for msg in messages if msg["role"] == "assistant"]
    return assistant_msgs + user_msgs

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages = limit_messages(st.session_state.messages)

    client = st.session_state.client
    stream = client.chat.completions.create(
        model = model_to_use,
        messages = st.session_state.messages,
        stream = True
    )
    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

def count_tokens(messages):
    return sum(len(msg['content'].split()) for msg in messages)

tokens_used = count_tokens(st.session_state.messages)
st.sidebar.write(f"Tokens passed: {tokens_used}")
