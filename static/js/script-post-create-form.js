    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('search_tagged_people');
        const taggedPeopleSelect = document.getElementById('id_tagged_people');
        const addTaggedPersonButton = document.getElementById('add_tagged_person');
        const taggedPeopleList = document.getElementById('tagged_people_list');
        const hiddenTaggedPeopleInput = document.getElementById('id_tagged_people_hidden');

        let taggedPeopleIds = [];  // Array to keep track of added user IDs

        // Search Users and Update Select Options
        searchInput.addEventListener('input', function() {
            const query = searchInput.value;

            if (query.length >= 2) {
                fetch(`/search-users/?query=${query}`, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Clear existing options
                    taggedPeopleSelect.innerHTML = '';

                    // Add new options from the fetched data
                    data.forEach(user => {
                        const option = document.createElement('option');
                        option.value = user.id;
                        option.textContent = user.name;
                        taggedPeopleSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            } else {
                // Clear the options if the input query is too short
                taggedPeopleSelect.innerHTML = '';
            }
        });

        // Add selected person to tagged people list
        addTaggedPersonButton.addEventListener('click', function() {
            const selectedOption = taggedPeopleSelect.selectedOptions[0];
            if (selectedOption && !taggedPeopleIds.includes(selectedOption.value)) {
                // Add selected person to tagged people array
                taggedPeopleIds.push(selectedOption.value);

                // Update the hidden input value (comma-separated user IDs)
                hiddenTaggedPeopleInput.value = taggedPeopleIds.join(',');

                // Add the person to the tagged people list
                const taggedPersonDiv = document.createElement('div');
                taggedPersonDiv.className = 'tagged-person';
                taggedPersonDiv.dataset.userId = selectedOption.value;
                taggedPersonDiv.textContent = selectedOption.textContent;

                // Add a remove button
                const removeButton = document.createElement('button');
                removeButton.type = 'button';
                removeButton.textContent = 'Remove';
                removeButton.className = 'remove-btn';
                removeButton.addEventListener('click', function() {
                    // Remove person from tagged people array
                    taggedPeopleIds = taggedPeopleIds.filter(id => id !== selectedOption.value);
                    hiddenTaggedPeopleInput.value = taggedPeopleIds.join(',');

                    // Remove the person from the tagged people list
                    taggedPersonDiv.remove();
                });

                taggedPersonDiv.appendChild(removeButton);
                taggedPeopleList.appendChild(taggedPersonDiv);
            }
        });
    });