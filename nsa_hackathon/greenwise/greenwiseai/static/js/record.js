let mediaRecorder_real;
let recordedChunks_real = [];
let isRecording_real = false;

const recordBtn = document.getElementById('recordBtn');

recordBtn.addEventListener('click', toggleRecording);

async function toggleRecording() {
    if (!isRecording_real) {
        startRecording_real();
    } else {
        stopRecording_real();
    }
}

async function startRecording_real() {
    recordedChunks_real = [];
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder_real = new MediaRecorder(stream);
        
        mediaRecorder_real.ondataavailable = function(event) {
            if (event.data.size > 0) {
                recordedChunks_real.push(event.data);
            }
        };
        
        // Only save when recording has fully stopped
        mediaRecorder_real.onstop = function() {
            saveRecording_real();
        };
        
        mediaRecorder_real.start();
        isRecording_real = true;
        
        recordBtn.className = 'stop';
        console.log("Recording started...");
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
    }
}

function stopRecording_real() {
    if (mediaRecorder_real && mediaRecorder_real.state !== "inactive") {
        mediaRecorder_real.stop();
        console.log("Recording stopped...");
    }
    isRecording_real = false;
    recordBtn.className = 'record';
}

function saveRecording_real() {
    console.log("Chunks recorded:", recordedChunks_real.length);

    const audioBlob = new Blob(recordedChunks_real, { type: 'audio/webm' }); // webm is safer
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
    "Seeds per acre": ["प्रति एकड बिउ", "बिउ"],
    "Planting depth": ["रोपाइँको गहिराइ", "मिलिमिटर"],
    "Row spacing": ["पंक्ति बीचको दुरी", "मिलिमिटर"],
    "Weekly irrigation": ["साप्ताहिक सिंचाइ", "पटक प्रति हप्ता"],
    "Rainfall this month": ["यस महिनाको वर्षा", "मिलिमिटर"],
    "Average temperature": ["औसत तापक्रम", "डिग्री सेल्सियस"],
    "Expected yield": ["अपेक्षित उत्पादन", "टन प्रति एकड"],
    "Expected revenue per acre": ["प्रति एकड अपेक्षित आम्दानी", "नेपाली रुपैयाँ"]
};

// Function to create data item HTML
function createDataItem(key, value) {
    const mapping = unitMapping[key];  // <- This line was missing!
    const translatedLabel = mapping[0];
    const unit = mapping[1];
    const unitSpan = ` <span class="unit">${unit}</span>`;
    
    return `
        <div class="data-item">
            <span class="data-label">${translatedLabel}: </span>
            <span class="data-value">${value}${unitSpan}</span>
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
    const dashboard = document.getElementById("dashboard");
    const record = document.getElementById("record");
    
    if (dashboard) {
        dashboard.classList.remove("d-none");
    }
    
    if (record) {
        record.classList.add("d-none");
    }
}