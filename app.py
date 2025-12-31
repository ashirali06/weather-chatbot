# ----- IMPORTS -----
import streamlit as st
import requests
import re

# ----- API KEYS -----
OPENWEATHER_KEY = st.secrets.get("OPENWEATHER_KEY", "")
HF_API_KEY = st.secrets.get("HF_API_KEY", "")

# ----- WEATHER TOOL -----
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    r = requests.get(url)

    if r.status_code != 200:
        return "City ka weather nahi mil saka."

    data = r.json()
    return f"{city.title()} ka temperature {data['main']['temp']}°C hai."

# ----- HUGGING FACE CHAT -----
def normal_chat(msg):
    if not HF_API_KEY:
        return "AI service unavailable."

    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": msg
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return "AI response error."

    data = response.json()

    try:
        return data[0]["generated_text"]
    except:
        return "AI response unavailable."

# ----- CHATBOT -----
def chatbot(user_input):
    if "weather" in user_input.lower():
        match = re.search(r"in ([a-zA-Z ]+)", user_input.lower())
        if match:
            return get_weather(match.group(1))
        return "Please city ka naam batayein."

    return normal_chat(user_input)

# ----- STREAMLIT UI -----
st.title("Weather Chatbot 🌦️")

user = st.text_input("Message")

if user:
    st.write(chatbot(user))
