// Enum for the modes of historyBuilder
const builderMode = Object.freeze({
    WIC: Symbol("WIC"),
    COMS: Symbol("COMS"),
})

// Enum for sorting order
const sortingOrder = Object.freeze({
    Ascending: Symbol("Ascending"),
    Desending: Symbol("Decending"),
})

/**
 * Given a list of meetings, sort and order by semester
 * @param {Object} meetings The list of meetings to order
 * @param {Symbol} sortOrder The order of the semesters that it will be returned.
 * @returns An array of Objects containing a semester date and all of the meetings in that semester. 
 */
function meetingsSortedBySemester(meetings, sortOrder){
    sortedMeetings = []

    meetings.forEach(meeting => {
        let findSemesterWithThisDate = sortedMeetings.find(semesterDate => semesterDate.semester === meeting.semester);
        if (findSemesterWithThisDate != undefined){
            findSemesterWithThisDate.meetings.push(meeting);
        } else {
            sortedMeetings.push({semester: meeting.semester, meetings: [meeting]});   
        } 
    });

    // Sort by order
    if (sortOrder == sortingOrder.Ascending){
        // Ascending - Earlest to latest
        sortedMeetings.sort((a, b) => parseFloat(a.semester) - parseFloat(b.semester))
    } else if (sortOrder == sortingOrder.Desending) {
        // Desending - Latest to earliest
        sortedMeetings.sort((a, b) => parseFloat(b.semester) - parseFloat(a.semester))
    }

    return sortedMeetings;
}

/**
 * Builds a list of all the semesters
 * @param {Symbol} mode The mode that will be entered in. 
 *  - If WIC is entered in, it will compute the meetings attended
 *  - If COMS is entered in, it will compute the points earned
 * @param {*} userValue The endpoint data of the user will be passed in
 * @param {*} totalValue The endpoint data of all users will be passed in.
 * @param {String} semester The semester that will be displayed
 */
function historyBuilder(mode, userValue, totalValue){

    //let sortedUserMeetings = meetingsSortedBySemester(userValue.profile.attendance);
    let sortedAllMeetings = meetingsSortedBySemester(totalValue.Meetings, sortingOrder.Desending);
    console.log(sortedAllMeetings);

    
    if (mode == builderMode.WIC){
        //console.log("WICMODE")
    } else if (mode == builderMode.COMS) {
        //console.log("COMSMODE")
    } else {
        console.log("Error: invalid mode entered in.")
    }

    // var newElement = `
    //     <div>
    //         <div>
    //             <p>
    //                 <b>Fall 2025:</b> Non-Active Member
    //             </p>
    //             <p>
    //                 <span>11/14 Total Points</span>
    //             </p>
    //         </div>
    //         <div>
    //             <img src="../static/images/awards.webp" alt="Award" >
    //         </div>
    //     </div>`

    //     container = document.getElementById("history-containers").appendChild();
}


/*
<div>
    <div>
        <p>
            <b>Fall 2025:</b> Non-Active Member
        </p>
        <p>
            <span>14 Total Points</span>
        </p>
    </div>
    <div>
        <img src="../static/images/awards.webp" alt="Award" >
    </div>
</div>
*/