import streamlit as st
import requests
from openai import OpenAI
from typing import List, Dict

if "messages" not in st.session_state:
    st.session_state.messages = []

client = OpenAI(api_key=st.secrets["API_KEY"])
API_NINJAS_KEY = st.secrets["API_KEY_N"]

def get_exercise_info(muscle: str) -> List[Dict]:
    """Fetch exercise information from API Ninjas."""
    url = "https://api.api-ninjas.com/v1/exercises"
    headers = {"X-Api-Key": API_NINJAS_KEY}
    params = {"muscle": muscle.lower()}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching exercise data: {str(e)}")
        return []

def generate_chat_response(messages: List[Dict]) -> str:
    """Generate response using OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I'm having trouble generating a response right now. Please try again."

def extract_muscle_group(text: str) -> str:
    """Extract muscle group from user input using OpenAI."""
    try:
        prompt = [
            {"role": "system", "content": "You are a fitness expert. Extract the muscle group from the following text. Reply with ONLY the muscle group name. If no muscle group is mentioned, reply with 'none'."},
            {"role": "user", "content": text}
        ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            max_tokens=50,
            temperature=0
        )
        return response.choices[0].message.content.lower()
    except Exception:
        return "none"

st.title("💪 FitChat - Your Personal Exercise Assistant")
st.write("Chat with me about exercises! I can help you find exercises for specific muscle groups and provide detailed instructions.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask me anything about exercises..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    muscle_group = extract_muscle_group(prompt)

    if muscle_group != "none":
        exercises = get_exercise_info(muscle_group)
        if exercises:
            exercise_info = "\n".join([
                f"• {ex['name']}: {ex['instructions'][:100]}..." 
                for ex in exercises[:3]
            ])

            messages = [
                {"role": "system", "content": "You are a knowledgeable and friendly fitness instructor. Provide helpful, encouraging advice about exercises. Keep responses concise and engaging."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": f"I found some exercises for {muscle_group}. Here are the details:\n{exercise_info}"}
            ]
        else:
            messages = [
                {"role": "system", "content": "You are a knowledgeable and friendly fitness instructor."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": f"While I couldn't find specific exercises for {muscle_group} in my database, I can provide general fitness advice."}
            ]
    else:
        messages = [
            {"role": "system", "content": "You are a knowledgeable and friendly fitness instructor."},
            {"role": "user", "content": prompt}
        ]

    with st.chat_message("assistant"):
        response = generate_chat_response(messages)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("💡 Tips")
    st.write("""
    - Ask about specific muscle groups like biceps, chest, or abs
    - Get exercise recommendations and instructions
    - Ask for workout tips and form advice
    - Questions about exercise frequency and intensity
    """)