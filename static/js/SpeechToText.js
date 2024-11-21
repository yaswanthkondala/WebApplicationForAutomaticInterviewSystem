export  default function recorder() {
if (!('webkitSpeechRecognition' in window)) {
    alert("Your browser does not support the Web Speech API. Please try Chrome.");
} else {
   
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true; 
    recognition.interimResults = true; 
    recognition.lang = 'en-US'; 

    const startButton = document.getElementById('micToggle');
    const stopButton = document.getElementById('micToggle');
    const resultElement = document.getElementById('question-text');
    
    recognition.onresult = function(event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        resultElement.textContent = transcript;
    };

    if(startButton.clicked === true) {
    
    startButton.addEventListener('click', () => {
        document.getElementById('botSpeech').innerHTML = "recording started";
        recognition.start();
        console.log("Speech recognition started");
    });
    }else{

    
    stopButton.addEventListener('click', () => {
        recognition.stop();
        document.getElementById('botSpeech').innerHTML = "recording started";
        console.log("Speech recognition stopped");
    });
    }

    
    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);
    };
}
}
