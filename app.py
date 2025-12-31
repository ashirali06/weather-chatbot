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

def normal_chat(msg):
    if not HF_API_KEY:
        return "AI service unavailable."

    url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": msg,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        return "AI service busy. Try again."

    data = response.json()

    # Case 1: model loading or HF error
    if isinstance(data, dict):
        if "error" in data:
            return "AI model is loading. Please try again in a few seconds."
        if "estimated_time" in data:
            return "AI is warming up. Try again shortly."

    # Case 2: normal response
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("generated_text", "No response from AI.")

    return "AI response unavailable."

