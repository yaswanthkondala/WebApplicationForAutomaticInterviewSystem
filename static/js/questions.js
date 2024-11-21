let questions = [];
window.currentQuestionIndex = 0;
let start=false;
window.q1=Array(24).fill(null);
function started(){
    window.location.href = "/interview";
    
}

function speakText(text) {
    const textInput = text;
    if ('speechSynthesis' in window) {
        
        const utterance = new SpeechSynthesisUtterance(textInput);

        
        const voices = speechSynthesis.getVoices();
        utterance.voice = voices.find(voice => voice.lang === 'en-US');

        
        utterance.pitch = 1; 
        utterance.rate = 1;  
        speechSynthesis.speak(utterance);
        utterance.onend = () => console.log("Speech has finished.");
        utterance.onerror = (event) => console.error("Speech error:", event);
    } else {
        alert("Your browser does not support speech synthesis.");
    }
}

function startTest() {
    const userId = sessionStorage.getItem('userId');
    
    if (!userId) {
        alert("User not logged in. Please log in first.");
        window.location.href = "/loginpage";
        return;
    }

    fetch('/get-questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({userId})
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            
            document.getElementById('name').innerHTML = result.name;
            questions = result.questions;
            console.log(questions);
            console.log(questions.length);
            window.n=questions.length
            document.getElementById('botSpeech').textContent = "started";
            // displayQuestion();
        } else {
            alert(result.message);
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        alert('Failed to load data');
    });
}

function play() {
    const avatarElement = document.getElementById("avathar");
    const currentAlt = avatarElement.alt;
    const pngPath = avatarElement.getAttribute("data-png");
    const gifPath = avatarElement.getAttribute("data-gif");

    if (currentAlt === "img") {
        avatarElement.src = gifPath;
        avatarElement.alt = "gif";
        
    } else {
        avatarElement.src = pngPath;
        avatarElement.alt = "img";
    }
    return;
}
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// Display the current question
async function displayQuestion() {
    if (currentQuestionIndex < questions.length) {
        const question = questions[currentQuestionIndex];
        play();
        window.q1[window.currentQuestionIndex]=`${question[0]}`
        await speakText(question[1]);
        await delay(5000);
        play();
        document.getElementById('question-text').textContent = `${question[1]}`;
        document.getElementById('subject').textContent = `${question[2]}`;
        document.getElementById('difficulty').textContent = `${question[3]}`;
    } else {
        alert("Test Completed!");
    }
}

// Load the next question
function nextQuestion() {
    window.currentQuestionIndex++;
    document.getElementById('question-text').textContent = `Click on "Ask Question" below to continue`;
}

// Attach event listeners
document.getElementById('startExam').addEventListener('click',started);
document.getElementById('askquestion').addEventListener('click', displayQuestion);
document.getElementById('nextquestion').addEventListener('click', nextQuestion);
document.getElementById('start').addEventListener('click', startTest);
