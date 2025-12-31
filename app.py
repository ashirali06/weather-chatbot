# ----- IMPORTS -----
import streamlit as st
import requests
import re
import google.generativeai as genai

# ----- API KEYS (SAFE) -----
OPENWEATHER_KEY = st.secrets.get("OPENWEATHER_KEY", "")
GEMINI_KEY = st.secrets.get("GEMINI_KEY", "")

# ----- WEATHER TOOL -----
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    r = requests.get(url)

    if r.status_code != 200:
        return "City ka weather nahi mil saka."

    data = r.json()
    return f"{city.title()} ka temperature {data['main']['temp']}°C hai."

# ----- GEMINI SETUP (OPTIONAL) -----
model = None
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-flash")

def normal_chat(msg):
    if not model:
        return "Main weather information provide kar sakta hoon. Weather poochiye."

    try:
        return model.generate_content(msg).text
    except Exception:
        return "AI response temporarily unavailable."

# ----- CHATBOT -----
def chatbot(user_input):
    if "weather" in user_input.lower():
        match = re.search(r"in ([a-zA-Z ]+)", user_input.lower())
        if match:
            return get_weather(match.group(1))
        return "City ka naam bataein."
    return normal_chat(user_input)

# ----- STREAMLIT UI -----
st.title("Weather Chatbot 🌦️")

user = st.text_input("Message")

if user:
    st.write(chatbot(user))

