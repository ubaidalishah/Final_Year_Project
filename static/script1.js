const postureBtn = document.querySelector(".posture-checking");

let muscle = null;
let exercise = null;
let body_weight = null;
let weight_lifted = null;

function setExercise(value) {
  exercise = value;
  if (value === 0 || value === 1) {
    muscle = 0;
  } else {
    muscle = 1;
  }
}

function submitForm(event) {
  event.preventDefault(); // Prevent the form from reloading the page

  body_weight = parseInt(document.getElementById("bodyWeight").value);
  weight_lifted = parseInt(document.getElementById("dumbbellWeight").value);

  fetch("/frontend_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      body_weight: body_weight,
      muscle: muscle,
      weight_lifted: weight_lifted,
      exercise: exercise,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        console.log("Frontend data submitted successfully");
        document.querySelector(".posture-checking").classList.remove("hidden");
        postureBtn.addEventListener("click", function () {
          window.location.href = "/predictions";
        });
      } else {
        console.error("Error:", data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}