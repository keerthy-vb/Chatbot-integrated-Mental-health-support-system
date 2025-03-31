document.addEventListener("DOMContentLoaded", function () {
    loadNotifications();
});

function loadNotifications() {
    fetch("/get_notifications")
        .then(response => response.json())
        .then(notifications => {
            const pendingList = document.getElementById("pendingNotifications");
            const completedList = document.getElementById("completedNotifications");

            pendingList.innerHTML = "";
            completedList.innerHTML = "";

            notifications.forEach(notification => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <span>${notification.text} - ${new Date(notification.time).toLocaleString()}</span>
                    <button onclick="markAsDone('${notification._id}', this)">✅ Done</button>
                    <button onclick="deleteNotification('${notification._id}', this)">🗑️ Delete</button>
                `;

                if (notification.status === "completed") {
                    li.style.opacity = "0.5";  // Faded effect for completed
                    completedList.appendChild(li);
                } else {
                    pendingList.appendChild(li);
                    checkMissedNotification(notification);
                }
            });
        })
        .catch(error => console.error("Error loading notifications:", error));
}

function markAsDone(notificationId, button) {
    fetch("/update_notification", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: notificationId, status: "completed" })
    })
    .then(response => response.json())
    .then(() => {
        button.parentElement.style.opacity = "0.5";
        document.getElementById("completedNotifications").appendChild(button.parentElement);
    })
    .catch(error => console.error("Error marking as done:", error));
}

function deleteNotification(notificationId, button) {
    fetch("/delete_notification", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: notificationId })
    })
    .then(response => response.json())
    .then(() => button.parentElement.remove())
    .catch(error => console.error("Error deleting notification:", error));
}

function checkMissedNotification(notification) {
    const currentTime = new Date().getTime();
    const notificationTime = new Date(notification.time).getTime();
    if (notificationTime < currentTime && notification.status !== "completed") {
        alert(`Missed Notification: ${notification.text}`);
    }
}
