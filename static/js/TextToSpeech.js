function speakText() {
    const textInput = document.getElementById('text-input').value;
    if ('speechSynthesis' in window) {
        
        const utterance = new SpeechSynthesisUtterance(textInput);

        
        const voices = speechSynthesis.getVoices();
        utterance.voice = voices.find(voice => voice.lang === 'en-US');

        
        utterance.pitch = 1; 
        utterance.rate = 1;  

        // Speak the text
        speechSynthesis.speak(utterance);

        // Optional: Handle events
        utterance.onend = () => console.log("Speech has finished.");
        utterance.onerror = (event) => console.error("Speech error:", event);
    } else {
        alert("Your browser does not support speech synthesis.");
    }
}
