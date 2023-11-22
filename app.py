from flask import Flask, request, jsonify
import speech_recognition as sr
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_data' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['audio_data']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)

        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='id-ID')
            return jsonify({'transcript': text}), 200
        except sr.UnknownValueError:
            return jsonify({'transcript': 'Could not understand the audio.'}), 200
        except sr.RequestError as e:
            return jsonify({'transcript': 'Error from Google Speech Recognition service; {0}'.format(e)}), 200
        except Exception as e:
            return jsonify({'transcript': 'An error occurred: {0}'.format(str(e))}), 500
        

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
