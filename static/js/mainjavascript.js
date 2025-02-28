function dropDown1() {
    document.getElementById("DropdownContent1").classList.toggle("show1");
}

function dropDown2() {
    document.getElementById("DropdownContent2").classList.toggle("show2");
}

function dropDown3() {
    document.getElementById("DropdownContent3").classList.toggle("show3");
}

window.onclick = function (event) {
    if (!event.target.matches('.dropbtn1')) {
        var dropdowns = document.getElementsByClassName("dropdown-content-large1");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show1')) {
                openDropdown.classList.remove('show1');
            }
        }
    }
    if (!event.target.matches('.dropbtn2')) {
        var dropdowns = document.getElementsByClassName("dropdown-content-large2");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show2')) {
                openDropdown.classList.remove('show2');
            }
        }
    }
    if (!event.target.matches('.dropbtn3')) {
        var dropdowns = document.getElementsByClassName("dropdown-content-medium");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show3')) {
                openDropdown.classList.remove('show3');
            }
        }
    }
}

// Function to handle file upload and display the data

function handleFileUpload() {
    const fileInput = document.getElementById('csv-file');
    const file = fileInput.files[0];
    const table = document.getElementById('dbTable');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const rows = e.target.result.split('\n');
            rows.forEach((row, index) => {
                const columns = row.split(',');
                if (columns.length > 1 && index > 0) { // Skip header row
                    const newRow = table.insertRow();
                    newRow.classList.add('dbTableRow');
                    newRow.innerHTML = `
                        <td>
                            <label class="container">
                                <input type="checkbox">
                                <span class="checkmark"></span>
                            </label>
                        </td>
                        <td>${columns[0]}</td>
                        <td>${columns[1]}</td>
                        <td>${columns[2]}</td>
                        <td>${columns[3]}</td>
                        <td>${columns[4]}</td>
                        <td>${columns[5]}</td>
                        <td>${columns[6]}</td>
                        <td>${columns[7]}</td>
                        <td>${columns[8]}</td>
                        <td class="dbTablePH"></td>
                        <td><img src="../static/images/options.png" width="16" /></td>
                    `;
                }
            });
        };
        reader.readAsText(file);
    } else {
        alert('Please select a CSV file first!');
    }
}

