document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ selfcare.js loaded successfully");  // Ensures script is loaded

    let getSuggestionsBtn = document.getElementById("getSuggestionsBtn");
    let categoryDropdown = document.getElementById("category");
    let suggestionsDiv = document.getElementById("suggestions");

    if (getSuggestionsBtn && categoryDropdown && suggestionsDiv) {
        getSuggestionsBtn.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent page reload

            let category = categoryDropdown.value;
            if (!category) {
                alert("⚠️ Please select a category before getting suggestions.");
                return;
            }

            fetch(`/selfcare/get_suggestions?category=${category}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsDiv.innerHTML = ""; // Clear previous results

                    if (data.length === 0) {
                        suggestionsDiv.innerHTML = "<p>No suggestions found for this category.</p>";
                        return;
                    }

                    data.forEach(item => {
                        let suggestionCard = `
                            <div class="suggestion">
                                <h3>${item.name}</h3>
                                <p>${item.description}</p>
                                <button onclick="saveActivity('${item.name}', '${item.type}')">Save</button>
                            </div>
                        `;
                        suggestionsDiv.innerHTML += suggestionCard;
                    });
                })
                .catch(error => console.error("❌ Error fetching suggestions:", error));
        });
    } else {
        console.error("❌ Missing required elements in HTML.");
    }
});

function saveActivity(name, type) {
    if (!name || !type) {
        console.error("❌ Invalid activity data.");
        return;
    }

    fetch("/selfcare/save_activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, type: type })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Activity saved successfully!");
        } else {
            alert("⚠️ Failed to save activity.");
        }
    })
    .catch(error => console.error("❌ Error saving activity:", error));
}
