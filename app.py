import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import base64

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Streamlit Config
st.set_page_config(page_title="Emergency AI Assistant", page_icon="🚑", layout="centered")

st.title("🚑 AI-Powered Emergency Assistant")
st.subheader("Get AI-guided, life-saving instructions in emergencies.")

with st.expander("❓ How does this work?"):
    st.write("""
    Describe your emergency situation, and our AI will guide you with quick, clear, and actionable steps to help until professionals arrive.
    """)

# Input Area
st.markdown("### Describe your emergency:")
emergency = st.text_area("E.g., Someone fainted, car accident, fire injury", height=100)

if st.button("Get AI Assistance", use_container_width=True):
    if emergency.strip():
        with st.spinner("AI is preparing your instructions..."):
            prompt = f"""
        You are an expert Emergency Response Assistant. Someone reported: '{emergency}'.

        Please provide:
        - Step-by-step instructions in simple language
        - Immediate actions to be taken
        - Warnings or precautions if needed
        Keep your response short, clear, and focused on saving lives.
        """
            response = model.generate_content(prompt)
            st.success("✅ Here's what to do:")
            st.write(response.text)
    else:
        st.warning("Please describe the emergency.")
    tts = gTTS(response.text)
    tts.save("response.mp3")

