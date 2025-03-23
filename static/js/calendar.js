<script>
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
                </script>