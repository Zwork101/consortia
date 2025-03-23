const listProfiles = async () => {
    const endpoint = "http://localhost:8080/admin/profiles/1";
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        console.log("Profiles loaded:", json.length);
        return json;
    } catch (error) {
        console.error(error.message);
        return [];
    }
}

const openEditProfileModal = async (userId) => {
    try {
        console.log("Opening modal for user ID:", userId);
        
        const modalElement = document.getElementById('editProfileModal');
        if (!modalElement) {
            console.error("Modal element not found in the document");
            alert("Error: Modal element not found");
            return;
        }
        
        const response = await fetch(`http://localhost:8080/profile/${userId}?org_id=1`);
        if (!response.ok) throw new Error('Profile fetch error');
        const data = await response.json();
        console.log("Profile data received:", data);
        
        // Populate modal form fields
        document.getElementById('edit-email').value = data.profile.email || '';
        document.getElementById('edit-first_name').value = data.profile.first_name || '';
        document.getElementById('edit-last_name').value = data.profile.last_name || '';
        document.getElementById('edit-rit_id').value = data.profile.rit_id || '';
        document.getElementById('edit-graduation_year').value = data.profile.graduation_year || '';
        document.getElementById('edit-degree').value = data.profile.degree || '';
        document.getElementById('edit-pronouns').value = data.profile.pronouns || '';
        document.getElementById('edit-avatar_path').value = data.profile.avatar_path || '';
        document.getElementById('edit-user-id').value = data.profile.profile_id;
        
        // Show modal by adding the show-modal class instead of setting style directly
        modalElement.classList.add('show-modal');
        console.log("Added show-modal class to modal");
        
    } catch (error) {
        console.error("Error in openEditProfileModal:", error);
        alert("Error loading profile: " + error.message);
    }
};

const addTableRows = (rows) => {
    const table = document.getElementById("dbTable");
    if (!table) {
        console.error("Table element not found!");
        return;
    }
    
    console.log(`Adding ${rows.length} rows to table`);
    
    rows.forEach(row => {
        const newElement = `
      <tr class="dbTableRow">
          <td>
              <label class="container">
                  <input type="checkbox">
                  <span class="checkmark"></span>
              </label>
          </td>
          <td>${row['profile']['first_name']}</td>
          <td>${row['profile']['last_name']}</td>
          <td>${row['profile']['membership']}</td>
          <td>${row['profile']['semesters']}</td>
          <td>${row['profile']['email']}</td>
          <td>${row['profile']['attendance'].filter(e => e['meeting_type'] == "GENERAL").length }</td>
          <td>${row['profile']['attendance'].filter(e => e['meeting_type'] == "COMMITTEE").length }</td>
          <td>${row['profile']['attendance'].filter(e => e['meeting_type'] == "SOCIAL").length }</td>
          <td>${row['profile']['attendance'].filter(e => e['meeting_type'] == "VOLUNTEER").length }</td>
          <td class="dbTablePH"></td>
          <td>
              <img src="../static/images/options.png" width="16" class="edit-profile-btn" data-user-id="${row['profile']['profile_id']}" />
          </td>
      </tr>
        `;
        table.insertAdjacentHTML('beforeend', newElement);
    });
    
    // Attach click listeners to options buttons
    document.querySelectorAll('.edit-profile-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const userId = e.currentTarget.getAttribute('data-user-id');
            openEditProfileModal(userId);
        });
    });
};

const applyFilters = () => {
    const sortBy = document.getElementById("filter-sort-by").value;
    const sortOrder = document.getElementById("filter-sort-order").value;
    const membership = document.getElementById("filter-membership").value;
    const semesters = document.getElementById("filter-semesters").value;
    const search = document.getElementById("search").value;
    
    console.log("Applying filters:", { sortBy, sortOrder, membership, semesters, search });
    
    const queryParams = new URLSearchParams();
    queryParams.append("filter-sort-by", sortBy);
    queryParams.append("filter-sort-order", sortOrder);
    queryParams.append("filter-membership", membership);
    queryParams.append("filter-semesters", semesters);
    if (search) {
        queryParams.append("search", search);
    }
    
    const endpoint = `http://localhost:8080/admin/profiles/1?${queryParams.toString()}`;
    
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const table = document.getElementById("orgMembers");
            // Remove existing rows (assuming rows have the class "dbTableRow")
            table.querySelectorAll(".dbTableRow").forEach(row => row.remove());
            addTableRows(data);
        })
        .catch(err => {
            console.error("Filter error:", err);
            alert("There was an error applying the filters. Please try again.");
        });
};

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, fetching profiles...');
    listProfiles().then(data => {
        addTableRows(data);
    });

    // Monitor filter form submission
    document.getElementById("filter-settings").addEventListener("submit", (e) => {
        e.preventDefault();
        applyFilters();
    });
    
    // Monitor search field input for real-time filtering
    document.getElementById("search").addEventListener("input", (e) => {
        // Debounce to avoid too many requests - wait 500ms after typing stops
        if (window.searchTimeout) clearTimeout(window.searchTimeout);
        window.searchTimeout = setTimeout(() => {
            applyFilters();
        }, 500);
    });
});