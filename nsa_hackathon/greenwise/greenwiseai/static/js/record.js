let mediaRecorder;
let recordedChunks = [];
let isRecording = false;

const recordBtn = document.getElementById('recordBtn');

recordBtn.addEventListener('click', toggleRecording);

async function toggleRecording() {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
}

async function startRecording() {
    recordedChunks = [];
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };
        
        // Only save when recording has fully stopped
        mediaRecorder.onstop = function() {
            saveRecording();
        };
        
        mediaRecorder.start();
        isRecording = true;
        
        recordBtn.className = 'stop';
        console.log("Recording started...");
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        console.log("Recording stopped...");
    }
    isRecording = false;
    recordBtn.className = 'record';
}

function saveRecording() {
    console.log("Chunks recorded:", recordedChunks.length);

    const audioBlob = new Blob(recordedChunks, { type: 'audio/webm' }); // webm is safer
    const title = 'New Recording';
    
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'recording.webm'); // match Django field name
    formData.append('title', title);
    
    fetch('/save/', { // add leading slash just to be safe
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("SUCCESS:", data);
            setTimeout(() => location.reload(), 1000);
        } else {
            console.log("FAIL:", data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
