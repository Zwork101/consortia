// Enum for the modes of historyBuilder
const builderMode = Object.freeze({
    WIC: Symbol("WIC"),
    COMS: Symbol("COMS"),
})

// Enum for sorting order
const sortingOrder = Object.freeze({
    Ascending: Symbol("Ascending"),
    Descending: Symbol("Descending"),
})

// Enum for semester term
const semesterTerm = Object.freeze({
    Spring: "Spring",
    Fall: "Fall",
})

// Enum for finding if user is active
const activeUser = Object.freeze({
    Active: "Active",
    NonActive: "Non-Active",
})

const awardHTML = `<img src="../static/images/awards.webp" alt="Award" >`;

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
    } else if (sortOrder == sortingOrder.Descending) {
        // Desending - Latest to earliest
        sortedMeetings.sort((a, b) => parseFloat(b.semester) - parseFloat(a.semester))
    }

    return sortedMeetings;
}

/**
 * Creates an Object that contains semester date data based on an semesterID.
 * @param {Number} semester The semesterID to pass in.
 * @returns An object containing term and year data.
 */
function semesterTermAndYear(semester){
    semesterDateObject = {}
    if (semester%10 == 0){
        semesterDateObject.term = semesterTerm.Spring;
    } else {
        semesterDateObject.term = semesterTerm.Fall;
    }
    semesterDateObject.year = Math.floor(semester/10);
    
    return semesterDateObject;
}

/**
 * Builds a list of all the semesters
 * @param {Symbol} mode The mode that will be entered in. 
 *  - If builderMode.WIC is entered in, it will compute the meetings attended
 *  - If builderMode.COMS is entered in, it will compute the points earned
 * @param {Object} userObject The object that represents the user 
 * @param {Object} allMeetingsObject The object that represents all meetings.
 */
function historyBuilder(mode, userObject, allMeetingsObject){

    let sortedUserMeetings = meetingsSortedBySemester(userObject.profile.attendance, sortingOrder.Descending);

    sortedUserMeetings.forEach(userSemester => {

        semesterDateData = semesterTermAndYear(userSemester.semester);
        let isUserActive = activeUser.NonActive;
        let awardValues, awardImage = ``
        if (mode == builderMode.WIC){
            //console.log("WICMODE")
            //let matchedSemester = sortedAllMeetings.find(semesterDate => semesterDate.semester === userSemester.semester);
        } else if (mode == builderMode.COMS) {
            //console.log("COMSMODE")

            // Set up total point Calculation
            let userSemesterPoints = getPointObject(userSemester.meetings);
            let userSemesterTotalPoints = pointSummer(userSemesterPoints);
            awardValues = `<span>${userSemesterTotalPoints}/${minPointRequirements} Total Points</span>`;

            // Set user to be active if they were active (by going to a mentorship meeting)
            if (userSemesterPoints.mentorshipPoints > 0){
                isUserActive = activeUser.Active;
            }
            // Award image if requirements were reached or exceeded
            if (userSemesterTotalPoints >= minPointRequirements){
                awardImage = awardHTML;
            }
        } else {
            console.log("Error: invalid mode entered in.");
        }

        table = document.getElementById("history-container");
        var semesterElement = `
            <div>
                <div>
                    <p>
                        <b>${semesterDateData.term} ${semesterDateData.year}:</b> ${isUserActive} Member
                    </p>
                    <p>
                        ${awardValues}
                    </p>
                </div>
                <div>
                    ${awardImage}
                </div>
            </div>`
        table.insertAdjacentHTML( 'beforeend', semesterElement);

    })
}