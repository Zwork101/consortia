// Helper function to get organization ID
function getCurrentOrgId() {
    // Check for organization ID in the page
    // Default to 1 for WiC or 2 for COMS
    return parseInt(document.getElementsByTagName("body")[0].dataset.org);

}

// Table type configurations for different data views
const tableConfigs = {
    profiles: {
        endpoint: (orgId) => `/admin/profiles/${orgId}`,
        getHeaders: (orgId) => {
            // Common headers for both organizations
            const commonHeaders = [
                { title: "", checkbox: true },
                { title: "FIRST NAME", sortKey: "First Name", dataKey: "profile.first_name", backendSortKey: "first_name" },
                { title: "LAST NAME", sortKey: "Last Name", dataKey: "profile.last_name", backendSortKey: "last_name" },
                { title: "MEMBERSHIP", dataKey: "profile.membership" },
                { title: "SEMESTER", sortKey: "Semesters", dataKey: "profile.semesters", backendSortKey: "semesters" },
                { title: "EMAIL ADDRESS", sortKey: "Email", dataKey: "profile.email", backendSortKey: "email" },
            ];
            
            // Organization-specific headers
            if (orgId === 1) { // WiC
                return [
                    ...commonHeaders,
                    { title: "GEN. MEETINGS", dataKey: "profile.attendance.general" },
                    { title: "COM. MEETINGS", dataKey: "profile.attendance.committee" },
                    { title: "SOCIAL EVENT", dataKey: "profile.attendance.social" },
                    { title: "VOLUNTEERING", dataKey: "profile.attendance.volunteering" },
                    { title: "", placeholder: true },
                    { title: "", actions: true }
                ];
            } else { // COMS
                return [
                    ...commonHeaders,
                    { title: "MENTORSHIP", dataKey: "profile.attendance.mentorship" },
                    { title: "VOLUNTEERING", dataKey: "profile.attendance.volunteering" },
                    { title: "ATTENDANCE", dataKey: "profile.attendance.general" },
                    { title: "MISC", dataKey: "profile.bonus_points" },
                    { title: "TOTAL POINTS", sortKey: "Points", dataKey: "profile.points", backendSortKey: "points" },
                    { title: "", placeholder: true },
                    { title: "", actions: true }
                ];
            }
        },
        renderRow: (row) => {
            // Generate mentorship, volunteering and other calculated fields
            // const mentorshipCount = row.profile.attendance ? 
            //     row.profile.attendance.filter(e => e.meeting_type === "MENTORSHIP").length : 0;
            // const volunteeringCount = row.profile.attendance ? 
            //     row.profile.attendance.filter(e => e.meeting_type === "VOLUNTEER").length : 0;
            // const generalCount = row.profile.attendance ? 
            //     row.profile.attendance.filter(e => e.meeting_type === "GENERAL").length : 0;
            // const committeeCount = row.profile.attendance ? 
            //     row.profile.attendance.filter(e => e.meeting_type === "COMMITTEE").length : 0;
            // const socialCount = row.profile.attendance ? 
            //     row.profile.attendance.filter(e => e.meeting_type === "SOCIAL").length : 0;
            
            // For WiC view, show different columns than COMS view
            if (getCurrentOrgId() === 1) { // WiC
                return `
                <tr class="dbTableRow">
                    <td>
                        <label class="container">
                            <input type="checkbox">
                            <span class="checkmark"></span>
                        </label>
                    </td>
                    <td>${row.profile.first_name}</td>
                    <td>${row.profile.last_name}</td>
                    <td>${row.profile.membership}</td>
                    <td>${row.profile.semesters}</td>
                    <td>${row.profile.email}</td>
                    <td>${row.profile.attendance.general}/14</td>
                    <td>${row.profile.attendance.committee}/6</td>
                    <td>${row.profile.attendance.social}</td>
                    <td>${row.profile.attendance.volunteering}</td>
                    <td class="dbTablePH"></td>
                    <td>
                        <img src="/static/images/options.png" width="16" class="edit-profile-btn" data-user-id="${row.profile.profile_id}" />
                    </td>
                </tr>`;
            } else { // COMS
                return `
                <tr class="dbTableRow">
                    <td>
                        <label class="container">
                            <input type="checkbox">
                            <span class="checkmark"></span>
                        </label>
                    </td>
                    <td>${row.profile.first_name}</td>
                    <td>${row.profile.last_name}</td>
                    <td>${row.profile.membership}</td>
                    <td>${row.profile.semesters}</td>
                    <td>${row.profile.email}</td>
                    <td>${row.profile.attendance.mentorship}</td>
                    <td>${row.profile.attendance.volunteering}</td>
                    <td>${row.profile.attendance.general}</td>
                    <td>${row.profile.bonus_points || 0}</td>
                    <td>${(row.profile.total_points || 0)}</td>
                    <td class="dbTablePH"></td>
                    <td>
                        <img src="/static/images/options.png" width="16" class="edit-profile-btn" data-user-id="${row.profile.profile_id}" />
                    </td>
                </tr>`;
            }
        }
    },
    events: {
        endpoint: (orgId) => `/admin/events/${orgId}`,
        headers: [
            { title: "EVENT NAME", sortKey: "Name", dataKey: "name", backendSortKey: "name" },
            { title: "DATE", sortKey: "Date", dataKey: "start_time", backendSortKey: "date" },
            { title: "TIME", sortKey: "Time", dataKey: "start_time", backendSortKey: "time" },
            { title: "TYPE", sortKey: "Type", dataKey: "meeting_type", backendSortKey: "type" },
            { title: "LOCATION", sortKey: "Location", dataKey: "location", backendSortKey: "location" },
            { title: "ATTENDEES", sortKey: "Attendees", dataKey: "attendance_count", backendSortKey: "attendees" },
            { title: "ATTENDANCE %", sortKey: "Percentage", dataKey: "attendance_percentage", backendSortKey: "percentage" }
        ],
        renderRow: (evt) => {
            return `
            <tr class="dbTableRow">
                <td>${evt.name}</td>
                <td>${new Date(evt.start_time).toLocaleDateString()}</td>
                <td>${new Date(evt.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
                <td>${evt.meeting_type}</td>
                <td>${evt.location}</td>
                <td>${evt.attendance_count}</td>
                <td>${evt.attendance_percentage}%</td>
            </tr>`;
        }
    }
};

// Generic function to render table headers
const renderTableHeaders = (tableType) => {
    const table = document.getElementById("dbTable");
    if (!table) {
        console.error("Table element not found!");
        return;
    }
    
    const config = tableConfigs[tableType];
    if (!config) {
        console.error(`Table configuration for ${tableType} not found!`);
        return;
    }
    
    let headerHTML = '<tr class="dbTableTop">';
    
    // Get headers based on current organization if this is the profiles view
    const headers = tableType === 'profiles' ? 
        config.getHeaders(getCurrentOrgId()) : 
        config.headers;
    
    headers.forEach(header => {
        if (header.checkbox) {
            headerHTML += '<th></th>';
        } else if (header.placeholder) {
            headerHTML += '<th class="dbTablePH"></th>';
        } else if (header.actions) {
            headerHTML += '<th></th>';
        } else {
            const sortAttr = header.sortKey ? `data-column="${header.sortKey}" data-backend-sort="${header.backendSortKey || header.sortKey}"` : '';
            headerHTML += `<th ${sortAttr}>${header.title}</th>`;
        }
    });
    
    headerHTML += '</tr>';
    table.innerHTML = headerHTML;
    
    // Add click event listeners to sortable headers
    document.querySelectorAll('#dbTable th[data-column]').forEach(th => {
        th.addEventListener('click', handleTableHeaderClick);
        th.style.cursor = 'pointer';
    });
};

// Generic function to load and render table data
const loadTableData = async (tableType, params = {}) => {
    const table = document.getElementById("dbTable");
    if (!table) {
        console.error("Table element not found!");
        return;
    }
    
    const config = tableConfigs[tableType];
    if (!config) {
        console.error(`Table configuration for ${tableType} not found!`);
        return;
    }
    
    // Clear existing rows (keep the header)
    const headerRow = table.rows[0];
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }
    
    // Show loading indicator
    const loadingRow = table.insertRow();
    const loadingCell = loadingRow.insertCell();
    loadingCell.colSpan = headerRow.cells.length;
    loadingCell.textContent = "Loading...";
    loadingCell.style.textAlign = "center";
    

    //  spinner element and load
    const spinner = document.createElement("div");
    spinner.classList.add("spinner");
    loadingCell.appendChild(spinner);


    // Build query parameters
    const queryParams = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
        if (value) queryParams.append(key, value);
    }
    
    try {
        const orgId = getCurrentOrgId();
        const endpoint = `${config.endpoint(orgId)}${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
        
        console.log(`Fetching data from: ${endpoint}`);
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error(`Response status: ${response.status}`);
        
        const data = await response.json();
        console.log(`${tableType} loaded:`, data.length);
        
        // Remove loading indicator
        table.deleteRow(1);
        
        // Render rows
        data.forEach(item => {
            const rowHTML = config.renderRow(item);
            table.insertAdjacentHTML('beforeend', rowHTML);
        });
        
        // Attach event handlers for action buttons if needed
        if (tableType === 'profiles') {
            document.querySelectorAll('.edit-profile-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const userId = e.currentTarget.getAttribute('data-user-id');
                    openEditProfileModal(userId);
                });
            });
        }
        
        return data;
    } catch (error) {
        console.error(`Error loading ${tableType}:`, error);
        
        // Remove loading indicator and show error
        table.deleteRow(1);
        const errorRow = table.insertRow();
        const errorCell = errorRow.insertCell();
        errorCell.colSpan = headerRow.cells.length;
        errorCell.textContent = `Error loading data: ${error.message}`;
        errorCell.style.textAlign = "center";
        errorCell.style.color = "red";
        
        return [];
    }
};

const loadProfiles = async (params = {}) => {
    // Determine which header set to use based on organization
    renderTableHeaders('profiles');
    return loadTableData('profiles', params);
};

const loadEvents = async (params = {}) => {
    renderTableHeaders('events');
    return loadTableData('events', params);
};

// Function to handle table header click for sorting
const handleTableHeaderClick = async (event) => {
    const headerCell = event.target.closest('th');
    if (!headerCell || !headerCell.dataset.column) return;
    
    // Get the column name from data attribute - use the backend sort key if available
    const column = headerCell.dataset.backendSort || headerCell.dataset.column;
    
    // Store the current state before we do any modifications
    const currentColumn = headerCell.dataset.column;
    const wasSorted = headerCell.hasAttribute('data-sorted');
    const currentDirection = headerCell.dataset.direction || 'none';
    
    // Determine the new direction
    let newDirection;
    if (wasSorted) {
        // If this column was already sorted, toggle direction
        newDirection = (currentDirection === 'asc') ? 'Descending' : 'Ascending';
        console.log(`Column ${currentColumn} was sorted ${currentDirection}, changing to ${newDirection}`);
    } else {
        // If this is a new column to sort, default to ascending
        newDirection = 'Ascending';
        console.log(`Sorting new column ${currentColumn} ${newDirection}`);
    }
    
    // Clear all sorting indicators and marks from all columns
    document.querySelectorAll('th[data-column]').forEach(th => {
        th.removeAttribute('data-sorted');
        th.removeAttribute('data-direction');
        th.querySelector('.sort-indicator')?.remove();
    });
    
    // Mark this column as sorted and set its direction
    headerCell.setAttribute('data-sorted', 'true');
    headerCell.setAttribute('data-direction', newDirection.toLowerCase() === 'ascending' ? 'asc' : 'desc');
    
    // Add visual indicator
    const indicator = document.createElement('span');
    indicator.className = 'sort-indicator';
    indicator.innerHTML = newDirection.toLowerCase() === 'ascending' ? ' ▲' : ' ▼';
    headerCell.appendChild(indicator);
    
    // Get parameters for current view
    const params = {
        "filter-sort-by": column,
        "filter-sort-order": newDirection
    };
    
    // Add search query if exists
    const searchInput = document.getElementById("search");
    if (searchInput && searchInput.value) {
        params.search = searchInput.value;
    }
    
    // Add filter parameters
    const filterForm = document.getElementById("filter-settings");
    if (filterForm) {
        const formData = new FormData(filterForm);
        for (let [key, value] of formData.entries()) {
            if (value !== "All") {
                params[key] = value;
            }
        }
    }
    
    console.log("Requesting server-side sort with params:", params);
    
    // Reload data with sorting parameters without re-rendering headers (preserving sort indicators)
    await loadTableData(currentView, params);
};

const applyFilters = async () => {
    console.log("applyFilters called");
    
    // Build filter parameters
    const params = {};
    
    // Add search query
    const searchQuery = document.getElementById("search")?.value;
    if (searchQuery) {
        params.search = searchQuery;
    }
    
    // Add filter form parameters
    const filterForm = document.getElementById("filter-settings");
    if (filterForm) {
        const formData = new FormData(filterForm);
        for (let [key, value] of formData.entries()) {
            if (value !== "All") {
                params[key] = value;
            }
        }
    }
    
    // Reload data with filter parameters for current view
    if (currentView === 'profiles') {
        await loadProfiles(params);
    } else if (currentView === 'events') {
        await loadEvents(params);
    }
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
        
        const org = getCurrentOrgId();
        
        const response = await fetch(`/profile/${org}/${userId}`);
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
        
        // Show modal by adding the show-modal class
        modalElement.classList.add('show-modal');
        modalElement.style.display = 'block';
        
    } catch (error) {
        console.error("Error in openEditProfileModal:", error);
        alert("Error loading profile: " + error.message);
    }
};

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

$(function() {
    $( document ).tooltip({
        track: true
    });
});

// Current view (default: profiles)
let currentView = 'profiles';

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing...');
    
    // Initialize search functionality
    const searchInput = document.getElementById("search");
    if (searchInput) {
        console.log("Search input found, adding event listener");
        searchInput.addEventListener("input", (e) => {
            console.log("Search input event fired", e.target.value);
            // Debounce to avoid too many requests
            if (window.searchTimeout) clearTimeout(window.searchTimeout);
            window.searchTimeout = setTimeout(() => {
                applyFilters();
            }, 500);
        });
    }
    
    // Initialize filter form
    const filterForm = document.getElementById("filter-settings");
    if (filterForm) {
        filterForm.addEventListener("submit", (e) => {
            e.preventDefault();
            console.log("Filter form submitted");
            applyFilters();
        });
    }
    
    // Initial data load
    loadProfiles();
    
    // Toggle dropdown view using the dropdown content option
    const dropdownOption = document.querySelector('#DropdownContent1 a');
    const dropdownButton = document.querySelector('.dropbtn1');
    if (dropdownOption && dropdownButton) {
        dropdownOption.addEventListener("click", (e) => {
            e.preventDefault();
            const org = getCurrentOrgId();
            const orgName = org === 1 ? "WiC" : "COMS";
            if (currentView === 'profiles') {
                loadEvents();
                dropdownButton.textContent = `${orgName} Attendance Data`;
                currentView = 'events';
            } else {
                loadProfiles();
                dropdownButton.textContent = `${orgName} Student Data`;
                currentView = 'profiles';
            }
        });
    }
    
    // Close button for edit profile modal
    const closeButtons = document.querySelectorAll('.modal .close');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal');
            if (modal) {
                modal.classList.remove('show-modal');
                modal.style.display = 'none';
            }
        });
    });
});