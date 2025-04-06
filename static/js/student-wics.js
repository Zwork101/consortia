const endpointOrganizationID = 1;
let maxEvents = 14;

/**
 * Creates an object of meeting data
 * @param {Array} listOfMeetings The array of meetings to be passed in
 * @returns An object of meeting data.
 */
function getMeetingData(listOfMeetings){

  const meetingObject = {
    socialEvents: 0,
    voluenteeringEvents: 0,
    committeeEvents: 0,
    generalEvents: 0,
    otherEvents: 0,
  }
  listOfMeetings.forEach(meeting =>{
    switch (meeting.meeting_type){
      case "SOCIAL":
        meetingObject.socialEvents += 1;
        break;
      case "VOLUNTEER":
        meetingObject.voluenteeringEvents +=1;
        break;
      case "COMMITTEE":
        meetingObject.committeeEvents +=1;
        break;
      case "GENERAL":
        meetingObject.generalEvents +=1;
        break;
      default:
        meetingObject.otherEvents +=1;
    }
  });
  return meetingObject;
}

/**
 * Draws the progress bar on the WIC webpage. This does not return anything.
 * @param {String} mainBarID The CSS ID of the main element to target.
 * @param {String} fillerBarID The CSS ID of the filler (gray) bar to target.
 * @param {Number} minMeetingsRequirements A number representing the minimum number of meetings one needs to attend.
 * @param {Number} meetingsAttended A number representing the actual number of meetings attended.
 * @param {Number} meetingMaxUIValue A number representing the upper bounds of the meeting bar. This is for the UI of the meeting bar.
 */
function drawProgressBar(mainBarID, fillerBarID, minMeetingsRequirements, meetingsAttended, meetingMaxUIValue){

  if (meetingsAttended < minMeetingsRequirements){
    let polyfillAmount = minSocialEventsRequirements - userMeetingsForCurrentSemester.socialEvents;
    // add code for gray polyfill
    document.getElementByID(fillerBarID).style.width = `${(polyfillAmount/meetingMaxUIValue)*100}%`;
  }

  document.getElementById(mainBarID).style.width = `${(meetingsAttended/meetingMaxUIValue)*100}%`;
}

/**
 * Display values for the bar on the "Current Semester" tab
 * @param {Object} userMeetingsForCurrentSemester An object representing the user with values from the most recent semester
 * @param {Object} allMeetingsForCurrentSemester An object representing all meetings with values from the most recent semester
 */
function showResults(userMeetingsForCurrentSemester, allMeetingsForCurrentSemester){
    
  document.getElementById("social-events").innerHTML = userMeetingsForCurrentSemester.socialEvents;
  document.getElementById("volunteering-events").innerHTML = userMeetingsForCurrentSemester.voluenteeringEvents;
  document.getElementById("committee-events").innerHTML = userMeetingsForCurrentSemester.committeeEvents;
  document.getElementById("general-events").innerHTML = userMeetingsForCurrentSemester.generalEvents;

  document.getElementById("total-social-events").innerHTML = allMeetingsForCurrentSemester.socialEvents;
  document.getElementById("total-volunteering-events").innerHTML = allMeetingsForCurrentSemester.voluenteeringEvents;
  document.getElementById("total-committee-events").innerHTML = allMeetingsForCurrentSemester.committeeEvents;
  document.getElementById("total-general-events").innerHTML = allMeetingsForCurrentSemester.generalEvents;
  
  // If the user exceeds the max events, we want to resize the bar so that it does not cause UI conflicts.
  let maximumUIValue = Math.max(
        userMeetingsForCurrentSemester.socialEvents,
        userMeetingsForCurrentSemester.voluenteeringEvents,
        userMeetingsForCurrentSemester.committeeEvents,
        userMeetingsForCurrentSemester.generalEvents
      ) 
  let meetingMaxUIValue;
  if (maximumUIValue > maxEvents) {
    meetingMaxUIValue = maximumUIValue;
  } else {
    meetingMaxUIValue = maxEvents;
  }

  let minSocialEventsRequirements = 1;
  let minVolunteeringEventsRequirements = 1;
  let minCommitteeEventsRequirements = 6;
  let minGeneralEventsRequirements = 14;

  drawProgressBar("social-total-points-bar", "social-min-requirements", minSocialEventsRequirements, userMeetingsForCurrentSemester.socialEvents, meetingMaxUIValue);
  drawProgressBar("volunteering-total-points-bar", "volunteering-min-requirements", minVolunteeringEventsRequirements, userMeetingsForCurrentSemester.voluenteeringEvents, meetingMaxUIValue);
  drawProgressBar("committee-total-points-bar", "committee-min-requirements", minCommitteeEventsRequirements, userMeetingsForCurrentSemester.committeeEvents, meetingMaxUIValue);
  drawProgressBar("general-total-points-bar", "general-min-requirements" , minGeneralEventsRequirements, userMeetingsForCurrentSemester.generalEvents, meetingMaxUIValue);
}

/**
 * Process the data for WIC.
 * @param {Object} studentData An Object representing the data of a student.
 * @param {Object} allMeetingData An Object that represents the data of all meetings.
 */
function processDataWIC(studentData, allMeetingData){
  let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
  let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);

  let userMeetingsForCurrentSemester = getMeetingData(attendance);
  let allMeetingsForCurrentSemester = getMeetingData(listOfAllMeetings);

  showResults(userMeetingsForCurrentSemester, allMeetingsForCurrentSemester);

  historyBuilder(builderMode.WIC, studentData, allMeetingData);
}


// const getStudentPoints = (endpointData) => {

//   let studentData = endpointData[0];
//   let allMeetingData = endpointData[1];

//   // Trim down list to current semester only
//   let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
//   let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);

//   let userMeetingsForCurrentSemester = getMeetingData(attendance);
//   let allMeetingsForCurrentSemester = getMeetingData(listOfAllMeetings);

//   showResults(userMeetingsForCurrentSemester, allMeetingsForCurrentSemester);

//   historyBuilder(builderMode.WIC, studentData, allMeetingData);
// }