import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Text-to-Voice Generator",
    page_icon="🔊",
    layout="centered"
)

st.title("🔊 AI Text-to-Voice Generator")
st.write("Convert your text into natural-sounding speech using AI.")

api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.info("Please configure your Groq API key in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

text = st.text_area(
    "Enter your text",
    placeholder="Type something you want to hear...",
    height=180
)

voice = st.selectbox(
    "Choose a voice",
   ["autumn", "diana", "hannah", "austin", "daniel", "troy"]
)

if st.button("🎙️ Generate Voice", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Generating your audio..."):
                response = client.audio.speech.create(
                    model="canopylabs/orpheus-v1-english",
                    voice=voice,
                    input=text.strip(),
                    response_format="wav"
                )

                audio_data = response.read()

            st.success("Your voice is ready!")
            st.audio(audio_data, format="audio/wav")

            st.download_button(
                "⬇️ Download Audio",
                data=audio_data,
                file_name="generated_voice.wav",
                mime="audio/wav",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Audio generation failed: {e}")
