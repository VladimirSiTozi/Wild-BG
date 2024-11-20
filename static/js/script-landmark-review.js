// Get modal element and buttons
const modal = document.getElementById("reviewModal");
const addReviewBtn = document.getElementById("addReviewBtn");
const closeBtn = document.querySelector(".close");

// Show modal when clicking 'Add review' button
addReviewBtn.addEventListener("click", () => {
    modal.style.display = "block";
});

// Close the modal when clicking 'X' button
closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

// Close the modal when clicking outside of the modal content
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});
