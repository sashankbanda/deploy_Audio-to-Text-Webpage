
# Audio to Text 📝🎧

This project allows users to upload audio files, which are then transcribed to text using automatic speech recognition (ASR) technology. The web app is built with Flask and utilizes Hugging Face's Whisper model for transcription.

## Features 🚀
- 🎤 Upload audio files and convert them to WAV format.
- 📝 Automatic transcription of the audio to text.
- 🔄 Real-time process updates during transcription.
- 💾 Simple and intuitive user interface to view progress and results.

## Tech Stack 🛠️
- **Backend**: Flask
- **ASR Model**: Hugging Face Whisper
- **Audio Processing**: PyDub, Librosa, NumPy
- **Frontend**: HTML, CSS, JavaScript

## File Structure 📁
```
D:.
│   app.py
│   requirements.txt
│
├───static
│   ├───css
│   │       styles.css
│   │
│   └───js
│           script.js
│
├───templates
│       index.html
│
└───uploads
```

## Installation 🛠️
1. Clone the repository:
    ```
    git clone https://github.com/sashankbanda/deploy_Audio-to-Text-Webpage.git
    ```

2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the app:
    ```
    python app.py
    ```

4. Open your browser and go to `http://127.0.0.1:5000/`.

## How to Use 📤
1. Open the web app.
2. Select an audio file from your device.
3. Click the "Upload" button.
4. View the real-time progress and get the transcription result when the process completes.

## Screenshots 🎨
![image](https://github.com/user-attachments/assets/bccc7d60-0e3c-405d-b083-edac780ab746)



## Contributing 👨‍💻
1. Fork the repository 🍴
    ```
    Click the "Fork" button at the top-right of the repository page on GitHub
    ```
2. Create a feature branch:
    ```
    git checkout -b feature-name
    ```
3. Commit changes:
    ```
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```
    git push origin feature-name
    ```
5. Open a pull request 📬
    ```
    Go to your repository on GitHub and click "Compare & pull request"
    ```

## License 📜
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by **Sashank Banda**
