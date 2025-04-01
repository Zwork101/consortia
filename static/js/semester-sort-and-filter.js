const ISODate = Object.freeze({
    YEAR: 0,
    MONTH: 1,
    EXTRA: 2,
})

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
    let thisYear = todaysDateAsArray[ISODate.YEAR];
    let thisMonth = todaysDateAsArray[ISODate.MONTH];

    var arrayOfMeetingsFromThisSemester = [];

    arrayOfMeetings.forEach( meeting => {
        
        // Same Year and Month
        if (
            (returnDateAsArray(meeting.start_time)[ISODate.YEAR] == thisYear) &&
            (
                ((thisMonth <= 6) && (returnDateAsArray(meeting.start_time)[ISODate.MONTH] <= 6)) ||
                ((thisMonth > 6) && (returnDateAsArray(meeting.start_time)[ISODate.MONTH] > 6))
            )) {
                arrayOfMeetingsFromThisSemester.push(meeting);
            } else {
                //console.log(meeting)
            }
        }
    )
    return arrayOfMeetingsFromThisSemester;
}
    
