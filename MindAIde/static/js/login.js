document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const errorMsg = document.getElementById("error-msg");
  
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const email = emailInput.value.trim();
      const password = passwordInput.value.trim();
  
      // Clear previous error
      errorMsg.textContent = "";
  
      if (!email || !password) {
        errorMsg.textContent = "Please enter both email and password!";
        return;
      }
  
      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      })
        .then((res) => {
          if (!res.ok) return res.json().then((data) => Promise.reject(data));
          return res.json();
        })
        .then((data) => {
          if (data.redirect) {
            window.location.href = data.redirect;
          }
        })
        .catch((err) => {
          if (err && err.redirect) {
            window.location.href = err.redirect; // fallback
          } else if (err && err.message) {
            errorMsg.textContent = err.message;
          } else {
            errorMsg.textContent = "Invalid credentials. Try again!";
          }
        });
    });
  });
  