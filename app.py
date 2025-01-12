from flask import Flask, request, jsonify, render_template, Response
import os
from pydub import AudioSegment
from transformers import pipeline
from librosa import load
import numpy as np
import time

app = Flask(__name__)

# Path to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the Hugging Face pipeline for audio transcription
transcriber = pipeline(
    model="openai/whisper-small",
    task="automatic-speech-recognition",
    device="cpu"
)

# Shared progress storage for real-time updates
progress = []

# Helper functions
def convert_to_wav(input_path, output_path, progress_callback):
    try:
        progress_callback("Converting to WAV...")
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        progress_callback("Conversion to WAV complete")
    except Exception as e:
        raise RuntimeError(f"Failed to convert to WAV: {e}")

def split_audio_with_overlap(audio, sr, max_duration=30, overlap=5):
    max_samples = int(max_duration * sr)
    overlap_samples = int(overlap * sr)
    start = 0
    chunks = []

    while start < len(audio):
        end = start + max_samples
        chunks.append(audio[start:end])
        start = end - overlap_samples
        if end > len(audio):
            break

    return chunks

def transcribe_audio(audio_path, progress_callback):
    try:
        progress_callback("Loading audio for transcription...")
        audio, sr = load(audio_path, sr=16000)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=0)

        progress_callback("Splitting audio into chunks...")
        audio_chunks = split_audio_with_overlap(audio, sr)

        full_transcription = []
        for i, chunk in enumerate(audio_chunks):
            progress_callback(f"Transcribing chunk {i + 1}/{len(audio_chunks)}...")
            result = transcriber(chunk)
            if isinstance(result, dict) and "text" in result:
                full_transcription.append(result["text"])

        progress_callback("Transcription complete")
        return " ".join(full_transcription).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe audio: {e}")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # Convert the audio file to WAV format
    wav_file = os.path.join(UPLOAD_FOLDER, "converted.wav")

    def progress_callback(msg):
        global progress
        progress.append(msg)

    convert_to_wav(filename, wav_file, progress_callback)

    # Transcribe the audio file
    transcription = transcribe_audio(wav_file, progress_callback)

    return jsonify({"transcription": transcription})

@app.route('/progress')
def progress_stream():
    def generate():
        while True:
            if progress:
                yield f"data: {progress.pop(0)}\n\n"
            time.sleep(1)

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
