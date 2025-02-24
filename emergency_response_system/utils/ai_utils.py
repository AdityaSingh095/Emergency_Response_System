import streamlit as st
import google.generativeai as genai
from config import GEMINI_API_KEY

def get_first_aid_response(disaster_type, input_text):
    """Get first aid response for disaster type using Gemini API"""
    if not disaster_type:
        return "Unable to determine emergency type. Please provide more information."

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-1.5-pro")
        prompt = f"What are the first-aid measures for a {disaster_type}? Context: {input_text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating first aid response: {e}")
        return "Unable to generate first aid response at this time."
