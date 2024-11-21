function submitLogin() {
    // Get form data
    const formData = {
        userid: document.getElementById('userid').value,
        password: document.getElementById('password').value
    };

    // Send data to the backend (Flask route)
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Login successful!");
            sessionStorage.setItem('loggedIn', 'true'); 
            sessionStorage.setItem('userId', data.userId);
            window.location.href = '/'; 
        } else {
            alert("Login failed: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred.");
    });
}


// function loginvalidation(){
//     var password = "12345";
//     const uspass=document.getElementById("password").value;
//     try{
//     if (uspass===password){
//         alert("logged success");
//         sessionStorage.setItem("loggedIn", "true");
//         window.location.href='/';
        
        

//     }else{
//         alert("login failed");

//     }}catch(e){
//         console.log(e);
//     }
    

// }



function submitForm() {
    // Get form data
    const formData = {
        userId: document.getElementById('userid').value,
        firstname: document.getElementById('firstname').value,
        lastname: document.getElementById('lastname').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        confirmPassword: document.getElementById('confirmpass').value,
        college: document.getElementById('college').value,
        phone_number: document.getElementById('phone_number').value,
        branch: document.getElementById('branch').value,
        yearofpass: document.getElementById('yearofpass').value,
        jobrole: document.getElementById('jobrole').value,
        experience: document.getElementById('experience').value,
        dateofbirth: document.getElementById('dateofbirth').value
    };
    if (formData.confirmPassword!=formData.password){
      alert("password and current password not matched please check");
      window.location.reload();
    }else{

    // Send data to the backend (Flask route)
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Registration successful!");
            window.location.href = '/'; // Navigate to another page
        } else {
            alert("Registration failed: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred.");
    });
  }
}


function validate() {
    if (sessionStorage.getItem("loggedIn") == "true") {
      
      document.getElementById("startexam").innerHTML = "Take Test";

     
      setTimeout(function () {
        window.location.href = "/instructionspage";
      }, 500); 
    } else {
      
      document.getElementById("startexam").innerHTML = "Login";

      
      setTimeout(function () {
        window.location.href = "/loginpage";
      }, 500); // Give time for innerHTML change to take effect
    }
  }
  document.getElementById('register').addEventListener('click', submitForm);
  document.getElementById('loginsubmit').addEventListener('click', submitLogin);

