const listProfiles = async (sortColumn = null, sortDirection = null) => {
    const endpoint = "/admin/profiles/1";
    const queryParams = new URLSearchParams();
    
    // Add sorting parameters if provided
    if (sortColumn) {
        queryParams.append("filter-sort-by", sortColumn);
        queryParams.append("filter-sort-order", sortDirection);
    }
    
    // Add existing filter values if available
    const searchInput = document.getElementById("search");
    if (searchInput && searchInput.value) {
        queryParams.append("search", searchInput.value);
    }
    
    // Add other filters if they exist and are set
    const membershipFilter = document.getElementById("filter-membership");
    if (membershipFilter && membershipFilter.value !== "All") {
        queryParams.append("filter-membership", membershipFilter.value);
    }
    
    const semestersFilter = document.getElementById("filter-semesters");
    if (semestersFilter && semestersFilter.value !== "All") {
        queryParams.append("filter-semesters", semestersFilter.value);
    }
    
    const finalEndpoint = `${endpoint}?${queryParams.toString()}`;
    
    try {
        const response = await fetch(finalEndpoint);
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

const refreshMeetingSelection = async (org) => {
    console.log("Refreshing meetings...")
    const meetingDropdown = document.getElementById("meeting-select");

    const meetings = await fetch(`/meetings/${org}`);
    if (!meetings.ok) {
        throw new Error(`Response status: ${meetings.status}`);
    }
    meetingDropdown.innerHTML = "";
    const data = await meetings.json();
    console.log(data);
    data["Meetings"].forEach(event => {
        const newEvent = `<option value="${event.event_id}">${event.name}</option>`
        meetingDropdown.insertAdjacentHTML('beforeend', newEvent);
    });
    meetingDropdown.removeAttribute("onmousedown");

}
// Function to handle table header click for sorting
const handleTableHeaderClick = async (event) => {
    const headerCell = event.target.closest('th');
    if (!headerCell || !headerCell.dataset.column) return;
    
    // Get the column name from data attribute
    const column = headerCell.dataset.column;
    
    // Toggle or set sort direction
    const currentDirection = headerCell.dataset.direction || 'asc';
    const newDirection = currentDirection === 'asc' ? 'Descending' : 'Ascending';
    
    // Remove sort indicators from all headers
    document.querySelectorAll('th[data-column]').forEach(th => {
        th.dataset.direction = '';
        th.querySelector('.sort-indicator')?.remove();
    });
    
    // Set new sort direction and add indicator to clicked header
    headerCell.dataset.direction = newDirection.toLowerCase() === 'ascending' ? 'asc' : 'desc';
    
    // Add visual indicator
    const indicator = document.createElement('span');
    indicator.className = 'sort-indicator';
    indicator.innerHTML = newDirection.toLowerCase() === 'ascending' ? ' ▲' : ' ▼';
    headerCell.appendChild(indicator);
    
    // Clear existing table rows
    const table = document.getElementById("dbTable");
    const headerRow = table.querySelector('.dbTableTop');
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }
    
    // Show loading indicator
    const loadingRow = table.insertRow();
    const loadingCell = loadingRow.insertCell();
    loadingCell.colSpan = headerRow.cells.length;
    loadingCell.textContent = "Loading...";
    loadingCell.style.textAlign = "center";
    
    // Fetch and display sorted data
    const profiles = await listProfiles(column, newDirection);
    
    // Remove loading indicator
    table.deleteRow(1);
    
    // Add new sorted rows
    addTableRows(profiles);
};

const openEditProfileModal = async (userId) => {
    try {
        console.log("Opening modal for user ID:", userId);
        
        const modalElement = document.getElementById('editProfileModal');
        if (!modalElement) {
            console.error("Modal element not found in the document");
            alert("Error: Modal element not found");
            return;
        }
        
        const response = await fetch(`profile/${userId}?org_id=1`);
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
    
    const endpoint = `/admin/profiles/1?${queryParams.toString()}`;
    
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const table = document.getElementById("dbTable");
            
            // Remove existing rows
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
    
    // Add click event listeners to table headers for sorting
    document.querySelectorAll('#dbTable th[data-column]').forEach(th => {
        th.addEventListener('click', handleTableHeaderClick);
        th.style.cursor = 'pointer';
    });
    
    // If no data-column attributes exist yet, add them after DOM is loaded
    if (!document.querySelector('#dbTable th[data-column]')) {
        const headerCells = document.querySelectorAll('#dbTable .dbTableTop th');
        const columnMappings = {
            1: "First Name",
            2: "Last Name", 
            3: "Membership",
            4: "Semesters", 
            5: "Email",
            6: "General Meetings",
            7: "Committee Meetings",
            8: "Social Events",
            9: "Volunteering",
            10: "Points"
        };
        
        // Skip first and last columns (checkbox and options)
        for (let i = 1; i < headerCells.length - 2; i++) {
            if (columnMappings[i]) {
                headerCells[i].dataset.column = columnMappings[i];
                headerCells[i].style.cursor = 'pointer';
                headerCells[i].addEventListener('click', handleTableHeaderClick);
            }
        }
    }
});