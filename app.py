import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import tempfile
import io
from google.api_core.exceptions import ResourceExhausted
import time

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def generate_audio(text):
    """Generate audio from text using gTTS"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(tmp_file.name)
            
            # Read the audio file
            with open(tmp_file.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            # Clean up
            os.unlink(tmp_file.name)
            return audio_bytes
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

def make_emergency_request(prompt):
    """Make API request with error handling"""
    try:
        response = model.generate_content(prompt)
        return response.text, None
    except ResourceExhausted:
        return None, "API rate limit exceeded. Please try again in a few minutes."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# Streamlit Configuration
st.set_page_config(
    page_title="Emergency AI Assistant", 
    page_icon="🚑", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Main Title
st.title("🚑 AI-Powered Emergency Assistant")
st.subheader("Get AI-guided, life-saving instructions in emergencies.")

# Critical Warning
st.error("⚠️ **CRITICAL**: For immediate life-threatening emergencies, call emergency services FIRST!")

# Emergency Contacts Sidebar
with st.sidebar:
    st.header("🚨 Emergency Contacts")
    
    st.subheader("🇮🇳 India")
    st.write("- **All Emergency**: 112")
    st.write("- **Police**: 100")
    st.write("- **Fire**: 101")
    st.write("- **Ambulance**: 108")
    
    st.subheader("🌍 International")
    st.write("- **USA**: 911")
    st.write("- **UK**: 999")
    st.write("- **EU**: 112")
    
    st.markdown("---")
    st.subheader("📱 Features")
    st.write("✅ AI-powered guidance")
    st.write("🔊 Audio instructions")
    st.write("📋 Step-by-step help")
    st.write("⚡ Quick response")

# How it works section
with st.expander("❓ How does this work?"):
    st.write("""
    **This AI Emergency Assistant provides:**
    - 🎯 **Immediate guidance** for emergency situations
    - 📝 **Step-by-step instructions** in simple language
    - 🔊 **Audio playback** so you can listen while helping
    - ⚠️ **Safety warnings** to prevent common mistakes
    
    **Important**: This is AI assistance only. Always call emergency services for serious situations!
    """)

# Main Input Section
st.markdown("### 📝 Describe your emergency:")
emergency = st.text_area(
    "Provide as much detail as possible",
    placeholder="E.g., 'Person collapsed and not breathing', 'Severe cut on arm bleeding heavily', 'House fire in kitchen'",
    height=120,
    help="The more details you provide, the better the AI can assist you"
)

# Action Button
if st.button("🆘 Get Emergency Instructions", type="primary", use_container_width=True):
    if emergency.strip():
        with st.spinner("🤖 AI is analyzing the situation and preparing instructions..."):
            # Enhanced prompt for better emergency response
            prompt = f"""
            EMERGENCY SITUATION: {emergency}
            
            You are an expert Emergency Medical Technician and First Aid instructor. Provide immediate, life-saving guidance.
            
            Format your response as:
            
            🚨 IMMEDIATE ACTIONS (RIGHT NOW):
            [2-3 most critical steps to take immediately]
            
            📋 STEP-BY-STEP INSTRUCTIONS:
            1. [First step]
            2. [Second step]
            3. [Continue with clear, numbered steps]
            
            ⚠️ IMPORTANT WARNINGS:
            [Critical things NOT to do]
            
            🏥 CALL EMERGENCY SERVICES IF:
            [Clear signs that professional help is needed immediately]
            
            Keep instructions simple, clear, and actionable. Prioritize safety and effectiveness.
            """
            
            # Make API request
            response_text, error = make_emergency_request(prompt)
            
            if response_text:
                # Display success message
                st.success("✅ Emergency Instructions Ready!")
                
                # Create two columns for better layout
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display the response
                    st.markdown("### 📋 Your Emergency Instructions:")
                    with st.container():
                        st.markdown(response_text)
                
                with col2:
                    st.markdown("### 🔊 Audio")
                    with st.spinner("Generating audio..."):
                        audio_bytes = generate_audio(response_text)
                        
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                            st.success("🎵 Audio ready!")
                        else:
                            st.warning("Audio generation failed")
                
                # Follow-up reminders
                st.markdown("---")
                st.warning("🔄 **Remember**: Monitor the situation continuously and call emergency services if the condition worsens!")
                
                # Quick actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔄 Get More Help", use_container_width=True):
                        st.rerun()
                with col2:
                    if st.button("📞 Show Emergency Numbers", use_container_width=True):
                        st.sidebar.success("👈 Check emergency numbers in sidebar")
                with col3:
                    if st.button("📋 Basic First Aid", use_container_width=True):
                        with st.expander("🩹 Basic First Aid Guide", expanded=True):
                            st.write("""
                            **Universal Steps:**
                            1. **Scene Safety** - Ensure area is safe
                            2. **Check Responsiveness** - Tap and shout
                            3. **Call for Help** - Emergency services
                            4. **Airway** - Clear if blocked
                            5. **Breathing** - Check for 10 seconds
                            6. **Circulation** - Check pulse, control bleeding
                            """)
                
            else:
                # Handle API errors
                st.error(f"❌ Unable to get AI assistance: {error}")
                
                # Provide fallback guidance
                st.warning("**Emergency Fallback Protocol:**")
                st.write("""
                1. **Stay Calm** - Take a deep breath
                2. **Ensure Safety** - Move to safety if needed
                3. **Call Emergency Services** - 108/112 (India) or local emergency number
                4. **Provide First Aid** - If trained and safe to do so
                5. **Monitor** - Watch for changes in condition
                6. **Prepare** - Gather information for emergency responders
                """)
                
                # Emergency contacts reminder
                st.info("📞 **Emergency Numbers**: 108 (Ambulance), 100 (Police), 101 (Fire), 112 (All Emergency)")
    
    else:
        st.warning("⚠️ Please describe the emergency situation to get assistance.")

# Quick Reference Guide
with st.expander("📚 Quick Emergency Reference"):
    tab1, tab2, tab3, tab4 = st.tabs(["🫁 Breathing", "🩸 Bleeding", "💔 Heart", "🔥 Burns"])
    
    with tab1:
        st.markdown("""
        **Choking (Conscious):**
        - 5 back blows between shoulder blades
        - 5 abdominal thrusts (Heimlich)
        - Repeat until object clears
        
        **Not Breathing:**
        - Check airway, tilt head back
        - 30 chest compressions, 2 rescue breaths
        - Continue CPR until help arrives
        """)
    
    with tab2:
        st.markdown("""
        **Severe Bleeding:**
        - Apply direct pressure with clean cloth
        - Elevate wound above heart if possible
        - Don't remove embedded objects
        - Apply pressure to pressure points
        - Call emergency services immediately
        """)
    
    with tab3:
        st.markdown("""
        **Heart Attack:**
        - Call emergency services immediately
        - Give aspirin if available and not allergic
        - Keep person calm and still
        - Monitor breathing and pulse
        
        **Stroke (F.A.S.T.):**
        - **Face** drooping, **Arms** weakness
        - **Speech** difficulty, **Time** to call 108
        """)
    
    with tab4:
        st.markdown("""
        **Burns:**
        - Cool with water for 10-20 minutes
        - Remove from heat source
        - Don't use ice or butter
        - Cover with clean, dry cloth
        - Seek medical attention for severe burns
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    🚑 Emergency AI Assistant | Always call professional emergency services for serious situations
    </div>
    """, 
    unsafe_allow_html=True
)