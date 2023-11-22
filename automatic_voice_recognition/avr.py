import speech_recognition as sr
import streamlit as st
from ml import rqa

# Initialize the recognizer
recognizer = sr.Recognizer()

def voice_recognition():
    # Use the microphone as source for input.
    with sr.Microphone() as source:
        st.markdown("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source)
        st.markdown("Please start speaking...")

        # Listen to the source
        audio = recognizer.listen(source)

        st.markdown("Recording stopped, processing...")

    # Recognize speech using Google's speech recognition
    try:
        # Recognize the speech
        response = recognizer.recognize_google(audio, language="id-ID")
        st.code("You said: " + response)
        return response
    except sr.UnknownValueError:
        st.error("I'm sorry, I could not understand what you were saying.")
    except sr.RequestError as e:
        st.error("Could not request results from the speech recognition service; {0}".format(e))

st.title("DPR Menjawab")

# Button to start the voice recognition
if st.button("Start Voice Recording"):
    txt = voice_recognition()
    if txt:
        st.markdown('RESULT:')
        st.markdown(rqa(txt)['result'])

