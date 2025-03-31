const submitQuiz = async (event) => {
    event.preventDefault(); // Prevent default form submission

    const email = document.getElementById("email")?.value || "";
    const name = document.getElementById("name")?.value || "";
    const user_id = localStorage.getItem("_id"); // Ensure user ID is retrieved
    // console.log("user  id from console", user_id);

    // if (!user_id) {
    //     alert("Error: User ID not found. Please log in again.");
    //     return;
    // }

    // Extract selected answers
    const answers = Array.from(document.querySelectorAll("input[type='radio']:checked"))
                         .map(input => {
                             const [category, score] = input.value.split(":");
                             return { category, score: parseInt(score) };
                         });

    const payload = {
        _id: user_id,
        email: email,
        name: name,
        answers: answers
    };

    console.log("📌 Sending data:", payload);  // Debugging

    try {
        const response = await fetch("/submit_quiz", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to submit quiz");
        }

        const data = await response.json();
        alert(`Quiz result: ${data.category}`);
        window.location.href = `/quiz_result?category=${data.category}`;
    } catch (error) {
        console.error("Error:", error);
        alert(`Error: ${error.message}`);
    }
};

// Attach event listener to button
document.getElementById("submitBtn").addEventListener("click", submitQuiz);
