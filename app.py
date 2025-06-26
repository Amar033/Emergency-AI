import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from google.api_core.exceptions import ResourceExhausted

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini Model with Flash (higher rate limits)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="Emergency AI Assistant", page_icon="🚑")
st.title("🚑 AI-Powered Emergency Assistant")
st.write("Get life-saving, AI-guided help during emergencies.")

# Add emergency disclaimer
st.warning("⚠️ **IMPORTANT**: This is AI assistance only. For life-threatening emergencies, call emergency services immediately!")

# Emergency contact numbers (customize based on location)
with st.expander("🚨 Emergency Contacts"):
    st.write("**India Emergency Numbers:**")
    st.write("- Police: 100")
    st.write("- Fire: 101") 
    st.write("- Ambulance: 108")
    st.write("- National Emergency: 112")

# User Input
emergency = st.text_input("Describe your emergency (e.g., 'Someone fainted', 'Fire injury')")

if st.button("Get AI Assistance"):
    if emergency.strip():
        with st.spinner("Generating emergency instructions..."):
            try:
                # Enhanced prompt for better emergency response
                prompt = f"""
                EMERGENCY SITUATION: {emergency}
                
                Please provide:
                1. IMMEDIATE actions to take RIGHT NOW
                2. Step-by-step first aid instructions
                3. When to call emergency services
                4. What NOT to do (common mistakes to avoid)
                5. How to prepare for emergency responders
                
                Keep instructions clear, numbered, and actionable. Prioritize safety.
                """
                
                response = model.generate_content(prompt)
                
                st.success("🆘 Emergency Instructions:")
                st.markdown(response.text)
                
                # Add follow-up reminder
                st.error("🚨 Remember: If this is a life-threatening emergency, call emergency services NOW!")
                
            except ResourceExhausted as e:
                st.error("⚠️ API Rate Limit Exceeded")
                st.write("The AI service is temporarily unavailable due to high usage.")
                st.write("**What to do now:**")
                st.write("1. Call emergency services immediately if life-threatening")
                st.write("2. Try again in a few minutes")
                st.write("3. Use the emergency contacts above")
                
                # Show basic first aid info
                with st.expander("📋 Basic Emergency Actions"):
                    st.write("""
                    **Universal Emergency Steps:**
                    1. Ensure scene safety
                    2. Check responsiveness 
                    3. Call for help (emergency services)
                    4. Check breathing and pulse
                    5. Begin appropriate first aid
                    6. Monitor until help arrives
                    """)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Please try again or contact emergency services directly.")
    else:
        st.warning("Please describe the emergency.")

# Add basic first aid reference
with st.expander("📚 Quick First Aid Reference"):
    st.write("""
    **Choking**: Back blows, then abdominal thrusts
    **Bleeding**: Direct pressure, elevate if possible
    **Burns**: Cool water for 10-20 minutes
    **Unconscious**: Recovery position, check breathing
    **Heart Attack**: Aspirin if available, call 108/112
    **Stroke**: F.A.S.T. test (Face, Arms, Speech, Time)
    """)