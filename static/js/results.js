// Sample data
const resultData = {
    id: "12345",
    name: "John Doe",
    role: "Student",
    correct: 8,
    wrong: 2,
    partial: 1,
    notAttempted: 3,
    score: 75
};


document.addEventListener('DOMContentLoaded', function () {
    // Function to generate result card
    function generateResultCard() {
        const userId = document.getElementById("id").value;  // Get user ID from input field
        if (!userId) {
            alert("Please enter a user ID.");
            return;
        }

        // Fetch the result from the server
        fetch('/sendresults', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId })  // Send the userId in the request body
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                const userdetails = result.userdetails;  // User details array
                const results1 = result.results;  // Results array
                
                console.log(results1);

                // Get the result card container
                const card = document.getElementById('result-card');
                
                // Ensure the result-card element is available before updating it
                if (card) {
                    card.innerHTML = `
                        <h2>Result Card</h2>
                        <div class="info"><span>ID:</span> ${results1[0]}</div>
                        <div class="info"><span>Name:</span> ${userdetails[0] + " " + userdetails[1]}</div>
                        <div class="info"><span>Role:</span> ${userdetails[2]}</div>
                        <div class="info"><span>Correct:</span> ${results1[1]}</div>
                        <div class="info"><span>Wrong:</span> ${results1[2]}</div>
                        <div class="info"><span>Partial:</span> ${results1[3]}</div>
                        <div class="info"><span>Not Attempted:</span> ${results1[4]}</div>
                        <div class="score">Score: ${results1[5]}</div>
                    `;
                } else {
                    console.error('Element with id "result-card" not found');
                }
            } else {
                alert(result.message);
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Failed to load data');
        });
    }

    // Bind the event listener to the button
    const resultButton = document.getElementById('result');
    if (resultButton) {
        resultButton.addEventListener('click', generateResultCard);
    }
});


// function generateResultCard() {
//     const userId = document.getElementById("id").value;
//     fetch('/sendresults', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({userId})
//     })
//     .then(response => response.json())
//     .then(result => {
//         if (result.status === 'success') {
            
//             document.getElementById('name').innerHTML = result.name;
//             userdetails = result.userdetails;
//             results1= result.results;
//             console.log(results1);
//             const card = document.getElementById('result-card');

//     card.innerHTML = `
//         <h2>Result Card</h2>
//         <div class="info"><span>ID:</span> ${results1[0]}</div>
//         <div class="info"><span>Name:</span> ${userdetails[0]+" "+userdetails[1]}</div>
//         <div class="info"><span>Role:</span> ${userdetails[2]}</div>
//         <div class="info"><span>Correct:</span> ${results1[1]}</div>
//         <div class="info"><span>Wrong:</span> ${results1[2]}</div>
//         <div class="info"><span>Partial:</span> ${results1[3]}</div>
//         <div class="info"><span>Not Attempted:</span> ${results1[4]}</div>
//         <div class="score">Score: ${results1[5]}</div>
//     `;
//         } else {
//             alert(result.message);
//         }
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//         alert('Failed to load data');
//     });

    
// }

// // Generate the card on page load
// generateResultCard(resultData);
