const submitQuiz = async () => {
    const email = document.getElementById("email").value;
    const name = document.getElementById("name").value;

    // Retrieve user_id from localStorage (if stored after login)
    const user_id = localStorage.getItem("user_id"); // Ensure this is stored when logging in

    if (!user_id) {
        alert("Error: User ID not found. Please log in again.");
        return;
    }

    // Get selected answers dynamically from radio buttons
    const answers = Array.from(document.querySelectorAll("input[type='radio']:checked"))
                         .map(input => parseInt(input.value));

    const response = await fetch("/submit_quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, email, name, answers }) // Include user_id
    });

    const data = await response.json();
    alert(`Quiz result: ${data.category}`);
};

document.getElementById("submitBtn").addEventListener("click", submitQuiz);
