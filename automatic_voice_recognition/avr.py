import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from ml import rqa

# Define a button in Bokeh and set up JavaScript to handle speech recognition.
stt_button = Button(label="Start Listening", width=100)

# The JavaScript code to handle the speech recognition start/stop toggle.
stt_button.js_on_event("button_click", CustomJS(code="""
    // Check if recognition is already defined and toggle it.
    if (window.recognition) {
        if (window.isListening) {
            window.recognition.stop();
            window.isListening = false;
            this.label = "Start Listening";  // Change button label to 'Start Listening'
        } else {
            window.recognition.start();
            window.isListening = true;
            this.label = "Stop Listening";  // Change button label to 'Stop Listening'
        }
    } else {
        // Initialize the speech recognition for the first click.
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'id-ID';
        window.recognition = recognition;
        window.isListening = true;  // Set a flag to track the listening state.
        this.label = "Stop Listening";

        recognition.onresult = function(e) {
            var value = e.results[e.resultIndex][0].transcript;
            if (e.results[e.resultIndex].isFinal) {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        };

        recognition.onspeechend = function() {
            recognition.stop();
        };

        recognition.onerror = function(event) {
            if (event.error !== "aborted") {  // Ignore the 'aborted' error since we're handling it.
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: 'Error occurred in recognition: ' + event.error}));
            }
        };

        recognition.start();
    }
"""))

# Use Streamlit to handle the speech recognition events and display the results.
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.subheader("PERTANYAAN:")
        st.write(result.get("GET_TEXT"))
        st.subheader("JAWABAN:")
        st.write(rqa(result.get("GET_TEXT"))['result'])
