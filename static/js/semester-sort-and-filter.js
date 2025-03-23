/**
 * 
 * @param {String} jsonDate The date in a JSON encoded 8601 string
 * @returns {Array} An array seperated by the dashes in the 8601 string. 
 * - The first item in the array is the year.
 * - The second item in the array is the month.
 * - The third item is the array is everything else.
 */
function returnDateAsArray(jsonDate){
    var returnArray = jsonDate.split(/[-]/gm);
    return returnArray;
}


/**
 * Return an array of meetings that happened from this semester 
 * @param {Array} arrayOfMeetings 
 */
function getMeetingsFromThisSemester(arrayOfMeetings){
    // print the date right now
    let now = (new Date()).toJSON();
    let todaysDateAsArray = returnDateAsArray(now);
    let thisYear = todaysDateAsArray[0];
    let thisMonth = todaysDateAsArray[1];

    var arrayOfMeetingsFromThisSemester = [];

    arrayOfMeetings.forEach( meeting => {
        
        // Same Year
        if (returnDateAsArray(meeting.start_time)[0] == thisYear){
            arrayOfMeetingsFromThisSemester.push(meeting);
            // Same Month
            if (thisMonth <= 6){
                console.log("Spring")
            } else {
                console.log("Fall")
            }
        }
        
    })
    return arrayOfMeetingsFromThisSemester;
}