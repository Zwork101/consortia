function dropDown1() {
    document.getElementById("DropdownContent1").classList.toggle("show1");
}

function dropDown2() {
    document.getElementById("DropdownContent2").classList.toggle("show2");
}

function dropDown3() {
    document.getElementById("DropdownContent3").classList.toggle("show3");
}

function dropDown4() {
    document.getElementById("DropdownContent4").classList.toggle("show4");
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
    if (!event.target.matches('.dropbtn4')) {
        var dropdowns = document.getElementsByClassName("dropdown-content-navbar");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show4')) {
                openDropdown.classList.remove('show4');
            }
        }
    }
}

$(document).ready(function () {
    let currentDate = new Date();

    function renderCalendar(date) {
        let month = date.toLocaleString('default', { month: 'long' });
        let year = date.getFullYear();
        $('#month-title').text(`${month} ${year}`);

        let firstDay = new Date(year, date.getMonth(), 1).getDay();
        let lastDate = new Date(year, date.getMonth() + 1, 0).getDate();

        let calendarHTML = "";
        let weekdays = ["S", "M", "T", "W", "T", "F", "S"];
        weekdays.forEach(day => {
            calendarHTML += `<div class="weekday">${day}</div>`;
        });
        for (let i = 0; i < firstDay; i++) {
            calendarHTML += '<div class="day empty"></div>';
        }
        for (let i = 1; i <= lastDate; i++) {
            calendarHTML += `<div class="day" data-date="${year}-${date.getMonth() + 1}-${i}">${i}</div>`;
        }
        $('.calendar-grid').html(calendarHTML);

        // Highlight today's date by default
        let today = new Date();
        if (today.getMonth() === date.getMonth() && today.getFullYear() === date.getFullYear()) {
            $('.day').each(function () {
                if ($(this).text() == today.getDate()) {
                    $(this).addClass('selected');
                }
            });
        }

        // Add click event to select a date
        $('.day').click(function () {
            $('.day').removeClass('selected');
            $(this).addClass('selected');
            let selectedDate = $(this).data('date');
            console.log(selectedDate); // Log the selected date
        });
    }

    renderCalendar(currentDate);

    $('#prev').click(function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    $('#next').click(function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });
});

function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}
// Drag and drop
const dropArea = document.getElementById('drop-area');

    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.style.backgroundColor = '#e0e0e0';
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.style.backgroundColor = '';
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.style.backgroundColor = '';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type === 'text/csv') {
                alert(`File uploaded: ${file.name}`);
                // You can add code here to further handle the file upload
            } else {
                alert('Only CSV files are allowed.');
            }
        }
    });
