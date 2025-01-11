const form = document.getElementById('upload-form');
const audioFileInput = document.getElementById('audio-file');
const progressBar = document.getElementById('upload-progress');
const progressStatus = document.getElementById('progress-status');
const processUpdates = document.getElementById('process-updates');
const transcriptionResult = document.getElementById('transcription-result');

// Handle form submission
form.addEventListener('submit', (event) => {
    event.preventDefault();
    const file = audioFileInput.files[0];

    if (!file) {
        alert("Please select an audio file.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    // Reset progress and result
    progressBar.value = 0;
    progressStatus.innerText = "Uploading file...";
    processUpdates.innerHTML = "";
    transcriptionResult.innerHTML = "";

    // Upload the file
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to upload file.");
            }
            return response.json();
        })
        .then(data => {
            if (data.transcription) {
                transcriptionResult.innerHTML = `<p>${data.transcription}</p>`;
            } else if (data.error) {
                transcriptionResult.innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            transcriptionResult.innerHTML = `<p>Error: ${error.message}</p>`;
        });
});

// Listen for real-time progress updates via SSE
const eventSource = new EventSource('/progress');
eventSource.onmessage = (event) => {
    const message = event.data;
    // Append the new message to process updates
    const newMessage = document.createElement('p');
    newMessage.innerText = message;
    processUpdates.appendChild(newMessage);

    // Scroll to the latest update
    processUpdates.scrollTop = processUpdates.scrollHeight;

    // Update progress bar (optional: use percentage updates if sent by server)
    if (message.includes('%')) {
        const percentage = parseInt(message.match(/\d+/), 10);
        if (!isNaN(percentage)) {
            progressBar.value = percentage;
        }
    }
};

// Handle SSE connection errors
eventSource.onerror = () => {
    progressStatus.innerText = "Lost connection to the server for real-time updates.";
    eventSource.close();
};
