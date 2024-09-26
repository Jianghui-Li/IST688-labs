import streamlit as st
import requests
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

if 'client' not in st.session_state:
    api_key = st.secrets["API_KEY"]
    st.session_state.client = OpenAI(api_key=api_key)
client = st.session_state.client

GPT_MODEL = "gpt-4o-mini"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print(colored("Unable to generate ChatCompletion response", "red"))
        print(f"Exception: {e}")
        return None

def get_current_weather(location, API_key):
    if "," in location:
        location = location.split(",")[0].strip()
    urlbase = "https://api.openweathermap.org/data/2.5/"
    urlweather = f"weather?q={location}&appid={API_key}"
    url = urlbase + urlweather
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200:
        return {"error": f"Failed to get data for {location}. Error: {data.get('message', 'Unknown error')}"}

    temp = data['main']['temp'] - 273.15
    feels_like = data['main']['feels_like'] - 273.15
    temp_min = data['main']['temp_min'] - 273.15
    temp_max = data['main']['temp_max'] - 273.15
    humidity = data['main']['humidity']
    
    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": round(humidity, 2)
    }

def weather_tool(location="Syracuse, NY"):
    api_key_1 = st.secrets["API_KEY_W"]
    weather_data = get_current_weather(location, api_key_1)
    if "error" in weather_data:
        return {"error": weather_data["error"]}
    return weather_data

def get_weather_and_clothing(location):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Please provide the weather for {location}."}
    ]
    
    tools = [
        {
            "name": "weather_tool",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country to get the weather for."
                    }
                },
                "required": ["location"]
            }
        }
    ]
    
    tool_choice = {"name": "weather_tool", "arguments": {"location": location}}

    response = chat_completion_request(messages=messages, tools=tools, tool_choice=tool_choice)

    if response is None or 'choices' not in response:
        return {"error": "Failed to get a response from the model."}
    
    return response

def get_clothing_suggestions_with_openai(weather_info):
    prompt = f"""
    The current weather in {weather_info['location']} is as follows:
    - Temperature: {weather_info['temperature']} °C
    - Feels like: {weather_info['feels_like']} °C
    - Minimum temperature: {weather_info['temp_min']} °C
    - Maximum temperature: {weather_info['temp_max']} °C
    - Humidity: {weather_info['humidity']}%

    Based on this weather, what clothing would you suggest someone wear today?
    """
    
    response = chat_completion_request(
        messages=[{"role": "user", "content": prompt}],
    )
    
    if response is None or 'choices' not in response:
        return "Unable to provide clothing suggestion at the moment."
    
    return response['choices'][0]['message']['content']

st.title("Weather and Clothing Suggestion Bot")

location = st.text_input("Enter a city (default: Syracuse, NY):", "Syracuse, NY")

if st.button("Get Weather and Suggest Clothing"):
    weather_response = get_weather_and_clothing(location)
    weather_data = weather_tool(location)
    
    if "error" in weather_data:
        st.error(weather_data["error"])
    else:
        st.write(f"Weather in {weather_data['location']}:")
        st.write(f"Temperature: {weather_data['temperature']} °C")
        st.write(f"Feels like: {weather_data['feels_like']} °C")
        st.write(f"Min Temp: {weather_data['temp_min']} °C")
        st.write(f"Max Temp: {weather_data['temp_max']} °C")
        st.write(f"Humidity: {weather_data['humidity']}%")

        suggestion = get_clothing_suggestions_with_openai(weather_data)
        st.subheader("Clothing Suggestion:")
        st.write(suggestion)
