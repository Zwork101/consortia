$( function() {
    var filter_dialog, filter_form;

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
                text: "Apply",
                // click: submit_filter_settings(filter_dialog),
                click: function() {
                    $("#filter-settings").submit;
                    filter_dialog.dialog('close');
                    console.log("filter box closed");
                }
            },
        ],
        // close:function() {
        //     filter_dialog.dialog('close');
            // filter_form[0].reset();
            // allFields.removeClass("ui-state-error")
        // }
    });
    // filter_form = filter_dialog.find("form").on("submit", function(event){
    //     event.preventDefault();
    //     submit_filter_settings();
    //     /*insert event here*/
    // });
    $("#filter-button").button().on("click", function() {
        filter_dialog.dialog('open');
        console.log("filter button pressed");
    });

    $( "#filter-sort-by" )
    .selectmenu()
    $( "#filter-sort-order" )
    .selectmenu()
    $( "#filter-membership" )
    .selectmenu()
    $( "#filter-semesters" )
    .selectmenu()
    $( "#filter-gen-meetings" )
    .selectmenu()
    $( "#filter-con-meetings" )
    .selectmenu()
    $( "#filter-social-event" )
    .selectmenu()
    $( "#filter-volunteering" )
    .selectmenu()

});