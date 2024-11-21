
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = stylesheetUrl;
    document.head.appendChild(link);
// Navbar HTML as a string
const navbarHTML = `
    <div class="navbar">
        <a href="#home" id="home-link">Home</a>
        <a href="#" id="login-link">Login</a>
        <a href="#" id="signup">Sign Up</a>
        <a href="#" id="results">Results</a>
        <a href="#about-us">About Us</a>
    </div>
`;

// Insert the navbar HTML into the container with id 'navbar'
document.getElementById('navbar').innerHTML = navbarHTML;
// document.getElementById('navbar1').innerHTML = navbarHTML;
// document.getElementById('navba2').innerHTML = navbarHTML;

// Function for handling login logic
function logged() {
    const loggedIn = sessionStorage.getItem("loggedIn");

    if (loggedIn === "true") {
        alert("Already logged in");
    } else {
        document.getElementById('login-link').href = "/loginpage";
    }
}

// Function for starting the exam
function startExam() {
    const loggedIn = sessionStorage.getItem("loggedIn");
    
    if (loggedIn === "true") {
        document.getElementById('startexam').href = "/instructionspage";
        // window.location.href = "/instructionspage";
    } else {
        alert("Please login first!");
        document.getElementById('startexam').href = "/loginpage";
    }
}
function signup(){
    document.getElementById('signup').href = "/registerpage";
}
function results(){
    document.getElementById('results').href = "/results";
}

// Add event listeners for the buttons
document.getElementById('login-link').addEventListener('click', logged);
document.getElementById('startexam').addEventListener('click', startExam);
document.getElementById('signup').addEventListener('click', signup);
document.getElementById('results').addEventListener('click', results);
