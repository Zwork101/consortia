$( function() {
    var filter_dialog, filter_form,
        create_meeting_dialog, create_meeting_form,
        import_data_dialog, import_data_form,
        send_email_dialog, send_email_form;

    // Create a success banner
    success_banner = $("<div id='success-banner' style='display:none; background-color: #F76902; color: white; padding: 10px; text-align: center; position: fixed; bottom: 20px; left: 40%; width: 20%; z-index: 9999; font-family: var(--main-font);'>Task completed successfully!</div>").appendTo("body");

  
    /*
    
    Filter dialog box
    
    */
    filter_dialog = $("#filter-dialog-box").dialog({
        autoOpen: false,
        height: 500,
        width: 600,
        modal: true,
        buttons: [
            {
                text: "Apply All",
                click: async function() {
                    // Properly submit the form
                    // $("#filter-settings").trigger("submit");
                    filter_dialog.dialog('close');
                    await applyFilters();
                    
                    // Close the dialog after the form is processed
                    console.log("filter box closed");
                }
            },
        ]
    });

    $("#filter-button").button().on("click", function() {
        filter_dialog.dialog('open');
        console.log("filter button pressed");
    });

    // Initialize the jQuery UI selectmenu widgets
    $("#filter-semester").selectmenu();
    $("#filter-sort-by").selectmenu();
    $("#filter-sort-order").selectmenu();
    $("#filter-membership").selectmenu();
    //$("#filter-semesters").selectmenu();
    //$("#filter-gen-meetings").selectmenu();
    //$("#filter-con-meetings").selectmenu();
    //$("#filter-social-event").selectmenu();
    //$("#filter-volunteering").selectmenu();


    /*
    
    Create Meeting dialog box
    
    */
    create_meeting_dialog = $("#create-meeting-dialog-box").dialog({
        autoOpen: false,
        height: 500,
        width: 600,
        modal: true,
        buttons: [
            {
                text: "Create Event",
                click: function() {
                    // Format date and times for backend
                    const date = $("#meeting-date").val();
                    const startTime = $("#meeting-time-start").val();
                    const endTime = $("#meeting-time-end").val();
                    
                    // Combine date and times into ISO strings
                    $("#meeting_start_time").val(formatDateTime(date, startTime));
                    $("#meeting_end_time").val(formatDateTime(date, endTime));
                    
                    // Properly submit the form
                    $("#create-meeting").submit();
                    
                    create_meeting_dialog.dialog('close');
                    console.log("create meeting box closed");
                    success_banner.text("Meeting created successfully!").fadeIn().delay(3000).fadeOut();
                }
            },
        ],
    });

    // Helper function to format date and time for backend
    function formatDateTime(date, timeStr) {
        if (!date) return '';
        
        // Parse the time string (e.g., "6:30pm")
        let hours = 0;
        let minutes = 0;
        let isPM = timeStr.toLowerCase().includes('pm');
        
        // Extract hours and minutes
        const timeParts = timeStr.replace(/(am|pm)/i, '').trim().split(':');
        hours = parseInt(timeParts[0], 10);
        if (timeParts.length > 1) {
            minutes = parseInt(timeParts[1], 10);
        }
        
        // Convert to 24-hour format
        if (isPM && hours < 12) hours += 12;
        if (!isPM && hours === 12) hours = 0;
        
        // Create a date object and format as ISO string
        const dateObj = new Date(date);
        dateObj.setHours(hours, minutes, 0, 0);
        return dateObj.toISOString();
    }
    
    $("#create-meeting-button").button().on("click", function() {
        create_meeting_dialog.dialog('open');
        console.log("create meeting button pressed");
    });

   $("#save-changes-button").click(function() {
    console.log("Button clicked!");
    success_banner.text("Changes saved successfully!").fadeIn().delay(3000).fadeOut();
});

    /*

    Create Import Data Dialog box

    */
    import_data_dialog = $("#import-data-dialog-box").dialog({
        autoOpen: false,
        height: 500,
        width: 600,
        modal: true,
            
            
        // close:function() {
        //     filter_dialog.dialog('close');
            // filter_form[0].reset();
            // allFields.removeClass("ui-state-error")
        // }
    });



    $("#import-data-button").button().on("click", function() {
        import_data_dialog.dialog('open');
        console.log("import meeting button pressed");
    });
   
    // Event Details Modal close functionality
    $(document).on('click', '#eventDetailsModal .close', function() {
        $('#eventDetailsModal').removeClass('show-modal').hide();
    });

    // Close modals when clicking outside of them
    $(window).on('click', function(event) {
        if ($(event.target).is('#eventDetailsModal')) {
            $('#eventDetailsModal').removeClass('show-modal').hide();
        }
    });

    $( "#data-event-name" )
    .selectmenu()
    $( "#data-event-date" )
    .selectmenu()

    /*

    Send Email Dialog box

    */
    send_email_dialog = $("#send-email-dialog-box").dialog({
        autoOpen: false,
        height: 500,
        width: 600,
        modal: true,
        buttons: [
            {
                text: "Send",
                // click: submit_filter_settings(filter_dialog),
                click: function() {
                    $("#send-email").submit;
                    send_email_dialog.dialog('close');
                    console.log("send email box closed");
                }
            },
        ],
        // close:function() {
        //     filter_dialog.dialog('close');
            // filter_form[0].reset();
            // allFields.removeClass("ui-state-error")
        // }
    });

    $("#send-email-button").button().on("click", function() {
        send_email_dialog.dialog('open');
        console.log("send email button pressed");
    });

    $('#notify-students').button().on("click", async function() {
        const org_id = document.getElementsByTagName("body")[0].dataset.org
        const awarded_users = document.querySelectorAll('.modal-rep-content input:checked');
        const data = []
        awarded_users.forEach((inp) => {
            data.push({
                profile_id: inp.dataset.profileId,
                award_id: inp.dataset.awardId
            })
        })

        const resp = await fetch(`/admin/awards/${org_id}/notify`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        const content = await resp.json();

        if (!content.success) {
            window.location.replace(content.url)
        } else {
            document.getElementById('modal-rep').style.display = "none";
        }
    })

    $('#modal-rep-Btn').button().on("click", async function() {
        const org_id = document.getElementsByTagName("body")[0].dataset.org
        const resp = await fetch(`/admin/profiles/${org_id}/worthy`);

        if (!resp.ok) {
              throw new Error(`Response status: ${resp.status}`);
        }

        const json = await resp.json();
        const table = document.getElementById("reward-table");
        table.innerHTML = "";

        json.forEach((recipient) => {
            table.insertAdjacentHTML('beforeend', `
            <tr class="dbTableRow">
                <td>
                    <label class="container">
                        <input checked type="checkbox" data-profile-id="${recipient.profile_id}" data-award-id="${recipient.award_id}">
                        <span class="checkmark"></span>
                    </label>
                </td>
                <td style="transform: translateX(-30px);"><b>${recipient.first_name} ${recipient.last_name}</b> has met the requirements for this award: <b>${recipient.award_name}</b></td>
                <td class="dbTablePH"></td>
                <td style="padding-right: 0px;">Active Semesters: <b>${recipient.award_requirement}</b></td>
            </tr>
            `);
        })
    });
    
    
    $('#modal-rew-Btn').button().on("click", async function () {
        const org_id = document.getElementsByTagName("body")[0].dataset.org;
        const resp = await fetch(`/admin/${org_id}/report`);
    
        if (!resp.ok) {
            throw new Error(`Response status: ${resp.status}`);
        }
    
        const data = await resp.json();
    
        // Count data for the upper report
        const upperReport = document.getElementById("report-upper");
        upperReport.innerHTML = `
            <p>Active Members: ${data.active_count_members}</p>
            <p>Inactive Members: ${data.inactive_count_members}</p>
            <p>Alumni Members: ${data.alumni_count_members}</p>
        `;
    
        // Filling in the Graduating Members table
        const gradTable = document.getElementById("graduation-table");
        gradTable.innerHTML = "";

        data.graduation_students.forEach((gradStudent) => {
            gradTable.insertAdjacentHTML("beforeend", `
                <tr class="dbTableRow">
                    <td></td>
                    <td>${gradStudent.first_name}</td>
                    <td>${gradStudent.last_name}</td>
                    <td>${gradStudent.membership ? "Active" : "Inactive"}</td>
                    <td>${gradStudent.semesters}</td>
                    <td>${gradStudent.email_address}</td>
                    <td class="dbTablePH"></td>
                    <td></td>
                </tr>
            `);
        });
    
        // Filling in the Active Members table
        const activeTable = document.getElementById("active-table");
        activeTable.innerHTML = "";

        data.active_students.forEach((activeStudent) => {
            activeTable.insertAdjacentHTML("beforeend", `
                <tr class="dbTableRow">
                    <td></td>
                    <td>${activeStudent.first_name}</td>
                    <td>${activeStudent.last_name}</td>
                    <td>${activeStudent.membership ? "Active" : "Inactive"}</td>
                    <td>${activeStudent.semesters}</td>
                    <td>${activeStudent.email_address}</td>
                    <td class="dbTablePH"></td>
                    <td></td>
                </tr>
            `);
        });

        document.querySelector(".semester-report-btn").addEventListener("click", function () {
            console.log("Download button clicked");
        
            const modal = document.getElementById("modal-rew");
            const downloadButton = document.querySelector(".semester-report-btn");
        
            modal.style.display = "block";
            modal.style.visibility = "visible";
            modal.style.opacity = "1";
        
            // Added because was causing a 404 error
            const font = document.createElement('link');
            font.rel = 'stylesheet';
            font.href = 'https://fonts.googleapis.com/css2?family=Roboto:wght@100;400;700&display=swap';
            document.head.appendChild(font);
        
            font.onload = function () {
                console.log("Roboto font loaded");
        
                const script = document.createElement('script');
                script.type = 'text/javascript';
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
        
                script.onload = function () {
                    console.log("html2pdf.js loaded successfully");
        
                    const element = document.getElementById("modal-rew");
                    if (!element) {
                        console.error("Modal element not found.");
                        return;
                    }
        
                    downloadButton.style.display = "none";
                    console.log("Modal text content:", element.textContent);
                    console.log("Generating PDF...");
        
                    const year = new Date().getFullYear();
                    const org_name = org_id === '1' ? "WIC" : "COMS";
        
                    const pdfLayout = {
                        margin: 0,
                        filename: `${org_name}_Report_${year}.pdf`,
                        image: { type: 'jpeg', quality: 0.98 },
                        html2canvas: { scale: 2 },
                        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
                    };
        
                    html2pdf().set(pdfLayout).from(element.innerHTML).save().finally(() => {
                        downloadButton.style.display = "block";
                        console.log("Generated PDF...");
                    });
                };

                document.body.appendChild(script);
            };
        });
    });

});

