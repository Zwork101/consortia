$( function() {
    var filter_dialog, filter_form,
        create_meeting_dialog, create_meeting_form,
        import_data_dialog, import_data_form,
        send_email_dialog, send_email_form;

    // Create a success banner
    success_banner = $("<div id='success-banner' style='display:none; background-color: #F76902; color: white; padding: 10px; text-align: center; position: fixed; top: 0; left: 40%; width: 20%; z-index: 9999;'>Task completed successfully!</div>").appendTo("body");

  
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
                click: function() {
                    // Properly submit the form
                    $("#filter-settings").trigger("submit");
                    
                    // Close the dialog after the form is processed
                    filter_dialog.dialog('close');
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
    $("#filter-semesters").selectmenu();
    $("#filter-gen-meetings").selectmenu();
    $("#filter-con-meetings").selectmenu();
    $("#filter-social-event").selectmenu();
    $("#filter-volunteering").selectmenu();


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
                // click: submit_filter_settings(filter_dialog),
                click: function() {
                    $("#create-meeting").submit;
                    create_meeting_dialog.dialog('close');
                    console.log("create meeting box closed");

                    success_banner.text("Meeting created successfully!").fadeIn().delay(3000).fadeOut();
                }
            },
        ],
        // close:function() {
        //     filter_dialog.dialog('close');
            // filter_form[0].reset();
            // allFields.removeClass("ui-state-error")
        // }
    });

    $("#create-meeting-button").button().on("click", function() {
        create_meeting_dialog.dialog('open');
        console.log("create meeting button pressed");
    });

   $("#save-changes-button").click(function() {
    console.log("Button clicked!");
    success_banner.text("Meeting created successfully!").fadeIn().delay(3000).fadeOut();
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



});