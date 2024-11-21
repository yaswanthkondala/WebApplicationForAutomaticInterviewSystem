// import { recorder } from "..js/SpeechToText";
var micOn = false;
let timeLeft=18000 // Initial state is "off"
let recognition;
// window.q=Array(24).fill(null).map(() => Array(2).fill(null));
 q = Array(24).fill(null);

// Check if the browser supports the Web Speech API
if (!('webkitSpeechRecognition' in window)) {
    alert("Your browser does not support the Web Speech API. Please try Chrome.");
} else {
    // Initialize the speech recognition object
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    // Event handler to display the recognized speech in the 'question-text' element
    recognition.onresult = function(event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        q[window.currentQuestionIndex]=transcript;
        document.getElementById('question-text').textContent = transcript;
    };

    // Handle any errors
    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);
        recognition.stop();
        console.log("Speech recognition stopped");
    };
}

// Function to toggle recording on/off
function toggleMic() {
    const micButton = document.getElementById('micToggle');
    micOn = !micOn;

    if (micOn) {
        // Start recording
        document.getElementById('botSpeech').textContent = "Recording started";
        micButton.textContent = "mic Off";
        micButton.classList.remove('btn-secondary');
        micButton.classList.add('btn-danger');
        recognition.start();
        console.log("Speech recognition started");
    } else {
        // Stop recording
        document.getElementById('botSpeech').textContent = "Recording stopped";
        micButton.textContent = "mic On";
        micButton.classList.remove('btn-danger');
        micButton.classList.add('btn-secondary');
        recognition.stop();
        console.log("Speech recognition stopped");
    }
}
document.getElementById('micToggle').addEventListener('click', toggleMic);
function startTimer() {
    const timerElement = document.getElementById('timer');
    const countdown = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(countdown);
            alert("Time's up! Submitting the test.");
            submitTest();
        }
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        timeLeft--;
    }, 1000);
}
function sendList(List) {
     // Example list

    fetch('/receive-list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ list: List ,user:sessionStorage.getItem('userId')})
    })
    .then(response => response.json())
    .then(data => console.log('Response from Flask:', data))
    .catch(error => console.error('Error:', error));
}
function submitTest() {
    alert("Test submitted successfully!");
    sendList(window.q1.map((item, index) => [item, q[index]]));
    window.location.href = "/review";
}


async function startWebcam() {
    const webcamElement = document.getElementById('webcam');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcamElement.srcObject = stream;
    } catch (err) {
        console.error("Error accessing webcam:", err);
        alert("Webcam access is required for the interview.");
    }
}


window.onload = function () {
    startWebcam();
    startTimer();
};
document.getElementById('submittest').addEventListener('click',submitTest);
