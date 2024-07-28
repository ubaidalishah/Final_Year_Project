document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.querySelector(".menu-btn");
  const navbarMenu = document.querySelector(".navbar-menu");
  const darkModeBtn = document.getElementById("dark-mode-toggle");
  const getStartedBtn = document.querySelector(".get-started-btn");
  let date = document.querySelector(".date");
  date.textContent = new Date().getFullYear();
  // setTimeout(function () {
  //   document.getElementById("preloader").style.display = "none";
  //   document.querySelector(".home-content").style.display = "block";
  //   document.querySelector(".navbar").style.display = "block";
  //   document.querySelector(".main3").style.display = "block";
  // }, 3000); // 3000 milliseconds = 3 seconds

  // Apply dark mode based on localStorage
  function applyDarkMode() {
    if (localStorage.getItem("dark-mode") === "enabled") {
      document.body.classList.add("dark-mode");
      document.querySelector(".navbar").classList.add("dark-mode");
      darkModeBtn.textContent = "Light Mode";
    } else {
      document.body.classList.remove("dark-mode");
      document.querySelector(".navbar").classList.remove("dark-mode");
      darkModeBtn.textContent = "Dark Mode";
    }
  }

  // Toggle dark mode and store preference in localStorage
  darkModeBtn.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    document.querySelector(".navbar").classList.toggle("dark-mode");
    if (document.body.classList.contains("dark-mode")) {
      localStorage.setItem("dark-mode", "enabled");
      darkModeBtn.textContent = "Light Mode";
    } else {
      localStorage.setItem("dark-mode", "disabled");
      darkModeBtn.textContent = "Dark Mode";
    }
  });

  // Event listener for menu button
  menuBtn.addEventListener("click", function () {
    navbarMenu.classList.toggle("active");
  });
  if (getStartedBtn)
    getStartedBtn.addEventListener("click", function () {
      window.location.href = "/exercises";
    });

  // Apply dark mode on page load
  applyDarkMode();
});
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("video").forEach((video) => {
    video.addEventListener("click", function () {
      const inputSection = document.getElementById("inputSection");
      const isActive = this.classList.toggle("active");

      // Reset other videos' borders
      document.querySelectorAll("video").forEach((v) => {
        if (v !== this) v.classList.remove("active");
      });

      // Toggle input section display
      if (isActive) {
        inputSection.style.display = "flex";
      } else {
        inputSection.style.display = "none";
      }
    });
  });
});

document.querySelector(".navbar-title").addEventListener("click", function () {
  window.location.href = "/";
});
document.querySelector(".bicep1").addEventListener("click", function () {
  window.location.href = "/bicep";
});
document.querySelector(".tricep1").addEventListener("click", function () {
  window.location.href = "/tricep";
});
