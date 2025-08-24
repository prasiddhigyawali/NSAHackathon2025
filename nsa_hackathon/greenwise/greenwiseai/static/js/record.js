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
            console.log("TRANSCRIPT: " + data.transcript);
            console.log("TRANSLATION: " + data.translation);
            console.log("SUCCESS:", data.data);
            populateData(data.data);
            showDashboard();
        } else {
            console.log("FAIL:", data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


const unitMapping = {
    "Seeds per acre": "seeds",
    "Planting depth": "mm",
    "Row spacing": "mm",
    "Weekly irrigation": "time/week",
    "Rainfall this month": "mm",
    "Average temperature": "°C",
    "Expected yield": "tons/acre",
    "Expected revenue per acre": "NPR"
};

// Function to format numbers
function formatNumber(value, key) {
    if (key === "Seeds per acre") {
        return value.toLocaleString();
    }
    if (key === "Expected revenue per acre") {
        return `${value}`;
    }
    return value.toString();
}

// Function to create data item HTML
function createDataItem(key, value) {
    const formattedValue = formatNumber(value, key);
    const unit = unitMapping[key];
    const unitSpan = key === "Expected revenue per acre" ? "" : ` <span class="unit">${unit}</span>`;
    
    return `
        <div class="data-item">
            <span class="data-label">${key}: </span>
            <span class="data-value">${formattedValue}${unitSpan}</span>
        </div>
    `;
}

// Function to populate data sections
function populateData(farmData) {
    // Populate planting data
    const plantingContainer = document.getElementById('planting-data');
    const plantingData = farmData['PLANTING DATA'];
    plantingContainer.innerHTML = Object.entries(plantingData)
        .map(([key, value]) => createDataItem(key, value))
        .join('');

    // Populate water data
    const waterContainer = document.getElementById('water-data');
    const waterData = farmData['WATER'];
    waterContainer.innerHTML = Object.entries(waterData)
        .map(([key, value]) => createDataItem(key, value))
        .join('');

    // Populate weather data
    const weatherContainer = document.getElementById('weather-data');
    const weatherData = farmData['WEATHER'];
    weatherContainer.innerHTML = Object.entries(weatherData)
        .map(([key, value]) => createDataItem(key, value))
        .join('');

    // Populate harvest data
    const harvestContainer = document.getElementById('harvest-data');
    const harvestData = farmData['PROJECTED HARVEST'];
    harvestContainer.innerHTML = Object.entries(harvestData)
        .map(([key, value]) => createDataItem(key, value))
        .join('');
}

function showDashboard() {
    document.getElementById("dashboard").classList.remove("d-none");
    document.getElementById("record").classList.add("d-none");
  }