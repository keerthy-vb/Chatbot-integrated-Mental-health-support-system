document.addEventListener("DOMContentLoaded", function () {
    const roleSelect = document.getElementById("role");
    const dynamicFields = document.getElementById("dynamic-fields");
    const registerForm = document.getElementById("register-form");

    roleSelect.addEventListener("change", function () {
        dynamicFields.innerHTML = ""; // Clear existing fields

        if (roleSelect.value === "Patient") {
            dynamicFields.innerHTML = `
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>

                <label for="age">Age:</label>
                <input type="number" id="age" name="age" required>

                <label for="gender">Gender:</label>
                <select id="gender" name="gender" required>
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>

                <label for="interests">Interests:</label>
                <input type="text" id="interests" name="interests">

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>

                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            `;
        } else if (roleSelect.value === "Therapist") {
            dynamicFields.innerHTML = `
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>

                <label for="specialization">Specialization:</label>
                <input type="text" id="specialization" name="specialization" required>

                <label for="qualification">Qualification:</label>
                <input type="text" id="qualification" name="qualification" required>

                <label for="experience">Experience (Years):</label>
                <input type="number" id="experience" name="experience" required>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>

                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            `;
        } else if (roleSelect.value === "Caretaker") {
            dynamicFields.innerHTML = `
                <label for="email">Caretaker Email:</label>
                <input type="email" id="email" name="email" required>

                <label for="patient_email">Patient's Email:</label>
                <input type="email" id="patient_email" name="patient_email" required>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>

                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            `;
        }
    });

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        if (jsonData.password !== jsonData.confirm_password) {
            alert("Passwords do not match!");
            return;
        }

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(jsonData),
            });

            const data = await response.json();
            alert(data.message);

            if (data.success) window.location.href = "/login";
        } catch (error) {
            alert("Something went wrong. Please try again.");
        }
    });
});
