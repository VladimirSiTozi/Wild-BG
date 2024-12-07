document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search_tagged_people');
    const taggedPeopleSelect = document.getElementById('id_tagged_people');
    const addTaggedPersonButton = document.getElementById('add_tagged_person');
    const taggedPeopleList = document.getElementById('tagged_people_list');
    const hiddenTaggedPeopleInput = document.getElementById('id_tagged_people_hidden');

    // Parse pre-rendered tagged user IDs from the hidden input
    let taggedPeopleIds = hiddenTaggedPeopleInput.value
        ? hiddenTaggedPeopleInput.value.split(',').filter(Boolean) // Parse existing IDs
        : [];

    function updateHiddenInput() {
        hiddenTaggedPeopleInput.value = taggedPeopleIds.join(',');
    }

    function addPersonToTaggedList(userId, userName) {
        if (taggedPeopleIds.includes(userId)) {
            alert(`${userName} is already tagged.`);
            return;
        }

        // Add the user ID to the array and update the hidden input
        taggedPeopleIds.push(userId);
        updateHiddenInput();

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
            taggedPeopleIds = taggedPeopleIds.filter((id) => id !== userId);
            updateHiddenInput();
            taggedPersonDiv.remove();
        });

        taggedPersonDiv.appendChild(removeButton);
        taggedPeopleList.appendChild(taggedPersonDiv);
    }

    searchInput.addEventListener('input', function () {
        const query = searchInput.value;

        if (query.length >= 2) {
            fetch(`/search-users/?query=${query}`, {
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
