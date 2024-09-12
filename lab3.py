import streamlit as st
from openai import OpenAI

st.title("My Lab3 Question Answering Chatbot")

openAI_model = st.sidebar.selectbox("Which Model?", ("mini", "regular"))
model_to_use = "gpt-4o-mini" if openAI_model == "mini" else "gpt-4o"

max_tokens = 1000

if 'client' not in st.session_state:
    api_key = st.secrets["API_KEY"]
    st.session_state.client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that explains things in a way a 10-year-old can understand."},
        {"role": "assistant", "content": "Hi there! What question can I help you with?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        chat_msg = st.chat_message(msg["role"])
        chat_msg.write(msg["content"])

def count_tokens(messages):
    return sum(len(msg['content'].split()) for msg in messages)

def limit_messages(messages, max_tokens):
    system_msg = [msg for msg in messages if msg["role"] == "system"]
    other_msgs = [msg for msg in messages if msg["role"] != "system"]

    user_msgs = [msg for msg in other_msgs if msg["role"] == "user"]
    assistant_msgs = [msg for msg in other_msgs if msg["role"] == "assistant"]

    if len(user_msgs) > 2:
        user_msgs = user_msgs[-2:]
        assistant_msgs = assistant_msgs[-2:]

    combined_msgs = []
    for user_msg, assistant_msg in zip(user_msgs, assistant_msgs):
        combined_msgs.append(user_msg)
        combined_msgs.append(assistant_msg)

    limited_messages = system_msg + combined_msgs

    token_count = count_tokens(limited_messages)
    while token_count > max_tokens and len(limited_messages) > 2:
        limited_messages.pop(0)
        token_count = count_tokens(limited_messages)

    return limited_messages

def get_bot_response(prompt, ask_more_info=True):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages = limit_messages(st.session_state.messages, max_tokens)
    
    client = st.session_state.client
    stream = client.chat.completions.create(
        model=model_to_use,
        messages=st.session_state.messages,
        stream=True
    )
    response = st.empty()
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response.markdown(full_response + "▌")
    response.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    if ask_more_info:
        response.markdown(full_response + "\n\nDO YOU WANT MORE INFO?")
        st.session_state.messages.append({"role": "assistant", "content": "DO YOU WANT MORE INFO?"})
    
    return full_response

def handle_user_input(prompt):
    if prompt.lower() == "yes":
        return get_bot_response("Please provide more information about the previous topic.")
    elif prompt.lower() == "no":
        return get_bot_response("What other question can I help you with?", ask_more_info=False)
    else:
        return get_bot_response(prompt)

if prompt := st.chat_input("What's your question?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    bot_response = handle_user_input(prompt)

tokens_used = count_tokens(st.session_state.messages)
st.sidebar.write(f"Tokens passed: {tokens_used}/{max_tokens}")
