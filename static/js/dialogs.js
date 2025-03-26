$( function() {
    var filter_dialog, filter_form,
        create_meeting_dialog, create_meeting_form,
        import_data_dialog, import_data_form,
        send_email_dialog, send_email_form;

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


});