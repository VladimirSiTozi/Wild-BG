// script-post-create-form.js
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search_tagged_people');
    const taggedPeopleSelect = document.getElementById('id_tagged_people');
    const addTaggedPersonButton = document.getElementById('add_tagged_person');
    const taggedPeopleList = document.getElementById('tagged_people_list');
    const form = taggedPeopleList.closest('form');

    // Track tagged people IDs
    let taggedPeopleIds = [];

    function addPersonToTaggedList(userId, userName) {
        if (taggedPeopleIds.includes(userId)) {
            alert(`${userName} is already tagged.`); // Fixed with backticks
            return;
        }

        // Add the user ID to the array
        taggedPeopleIds.push(userId);

        // Create a hidden input for the tagged person
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'tagged_people';
        hiddenInput.value = userId;
        form.appendChild(hiddenInput);

        // Create a new div for the tagged person
        const taggedPersonDiv = document.createElement('div');
        taggedPersonDiv.className = 'tagged-person';
        taggedPersonDiv.dataset.userId = userId;
        taggedPersonDiv.textContent = userName;

        // Add a "Remove" button
        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.textContent = 'Remove';
        removeButton.className = 'remove-btn';
        removeButton.addEventListener('click', function () {
            // Remove the user ID from the array
            taggedPeopleIds = taggedPeopleIds.filter((id) => id !== userId);
            // Remove the hidden input
            const inputs = form.querySelectorAll('input[name="tagged_people"]');
            inputs.forEach(input => {
                if (input.value === userId) {
                    input.remove();
                }
            });
            // Remove the tagged person div
            taggedPersonDiv.remove();
        });

        taggedPersonDiv.appendChild(removeButton);
        taggedPeopleList.appendChild(taggedPersonDiv);
    }

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;

        if (query.length >= 2) {
            fetch(`/search-users/?query=${encodeURIComponent(query)}`, {  // Fixed with backticks
                method: 'GET',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            })
                .then((response) => response.json())
                .then((data) => {
                    taggedPeopleSelect.innerHTML = ''; // Clear existing options

                    // Populate the dropdown with fetched users
                    data.forEach((user) => {
                        const option = document.createElement('option');
                        option.value = user.id;
                        option.textContent = user.name;
                        taggedPeopleSelect.appendChild(option);
                    });
                })
                .catch((error) => console.error('Error fetching users:', error));
        } else {
            taggedPeopleSelect.innerHTML = ''; // Clear options if the input is too short
        }
    });

    addTaggedPersonButton.addEventListener('click', function () {
        const selectedOption = taggedPeopleSelect.selectedOptions[0];
        if (!selectedOption) {
            alert('Please select a person to tag.');
            return;
        }

        const userId = selectedOption.value;
        const userName = selectedOption.textContent;

        addPersonToTaggedList(userId, userName);

        // Clear dropdown and search input after adding a user
        taggedPeopleSelect.selectedIndex = -1;
        searchInput.value = '';
    });
});
