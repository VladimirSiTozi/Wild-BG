document.addEventListener('DOMContentLoaded', () => {
    // Get all reply buttons
    const replyButtons = document.querySelectorAll('.reply-btn');

    replyButtons.forEach(replyButton => {
        replyButton.addEventListener('click', function() {
            // Get parent comment element
            const commentContent = replyButton.parentElement;

            // Show reply section and hide reply button
            const replySection = commentContent.querySelector('.reply-section');
            replySection.style.display = 'block';
            replyButton.style.display = 'none';

            // Add event listeners to send and cancel buttons
            const sendButton = commentContent.querySelector('.send-btn');
            const cancelButton = commentContent.querySelector('.cancel-btn');

            cancelButton.addEventListener('click', () => {
                // Hide reply section and show reply button again
                replySection.style.display = 'none';
                replyButton.style.display = 'block';
            });

            // Optionally, add functionality to the send button
            sendButton.addEventListener('click', () => {
                // You can add functionality here for handling the reply, e.g., sending to a server
                alert('Reply sent!');

                // Hide reply section and show reply button after sending reply
                replySection.style.display = 'none';
                replyButton.style.display = 'block';
            });
        });
    });
});
