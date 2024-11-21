document
          .getElementById("submitFeedback")
          .addEventListener("click", () => {
            const rating = document.querySelector(
              'input[name="rating"]:checked'
            );
            if (rating) {
              alert(`Thank you! You rated ${rating.value} star(s).`);
            } else {
              alert("Please select a rating.");
            }
          });