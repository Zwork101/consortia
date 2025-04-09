const org = document.getElementsByTagName("body")[0].dataset.org;
const eventList = $( "#events" );
const eventTemplate = $( "#event-template" );

const displayEvent = (eventName, eventDate, eventType, eventDescription) => {
    const newEvent = eventTemplate.clone();
    const lastEvent = eventList.find(".event:last-of-type");

    newEvent.find(".event-name").text(eventName);
    newEvent.find(".event-time").text(
        eventDate.toString()
    )
    newEvent.find(".description").text(eventDescription)
    let color;
    if (eventType == "GENERAL") {
        color = "var(--label-yellow)";
    } else if (eventType == "SOCIAL") {
        color = "var(--label-purple)";
    } else if (eventType == "COMMITTEE") {
        color = "var(--label-green)";
    } else if (eventType == "VOLUNTEER") {
        color = "var(--label-blue)";
    } else if (eventType == "MENTORSHIP") {
        color = "var(--label-purple)";
    }

    newEvent.attr("id", "")
    newEvent.css("borderColor", color);
    newEvent.insertAfter(lastEvent);
    newEvent.attr("hidden", false);
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
        $('.day').click(async function () {
            $('.day').removeClass('selected');
            $(this).addClass('selected');
            let selectedDate = new Date($(this).data('date'));
            
            const resp = await fetch(`/meetings/${org}?` +
                new URLSearchParams({
                    selected: selectedDate.toISOString()
                }).toString()
            )

            const meetings = await resp.json();

            $(".event:not([hidden])").remove();

            meetings.Meetings.forEach((meeting) => {
                displayEvent(meeting.name, new Date(meeting.start_time), meeting.meeting_type, meeting.description)
            })

            console.log(meetings)
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
