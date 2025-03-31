const endpointOrganizationID = 1;
let maxEvents = 14;

// // user variables
// let socialEvents = 0;
// let voluenteeringEvents = 0;
// let committeeEvents = 0;
// let generalEvents = 0;
// let otherEvents = 0;

// // all variables 
// let allSocialEvents = 0;
// let allVoluenteeringEvents = 0;
// let allCommitteeEvents = 0;
// let allGeneralEvents = 0;
// let allOtherEvents = 0;

// const getProfile = async () => {
//   const userId = document.getElementsByTagName("body")[0].dataset.profileId;
// 	const profileEndpoint = `/profile?org=1`;
//   const meetingsEndpoint = "/meetings/1";
// 	try {
//       var endpointList = []
//     	const response = await fetch(profileEndpoint);
// 	    if (!response.ok) {
// 	      throw new Error(`Response status: ${response.status}`);
// 	    }

// 	    const json = await response.json();
//       endpointList.push(json);

// 	    const response2 = await fetch(meetingsEndpoint);
// 	    if (!response2.ok) {
// 	      throw new Error(`Response status: ${response2.status}`);
// 	    }

// 	    const json2 = await response2.json();
//       endpointList.push(json2);
      
//       return endpointList;
// 	 } catch (error) {
// 	    console.error(error.message);
//   }
// }

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
 * Display values for the bar on the "Current Semester" tab
 * @param {Object} userMeetingsForCurrentSemester An object representing the user with values from the most recent semester
 * @param {Object} allMeetingsForCurrentSemester An object representing all meetings with values from the most recent semester
 */
function showResults(userMeetingsForCurrentSemester, allMeetingsForCurrentSemester){
  // Draw bars and display numbers.
  document.getElementById("social-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.socialEvents/maxEvents)*100}%`;
  document.getElementById("volunteering-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.voluenteeringEvents/maxEvents)*100}%`;
  document.getElementById("committee-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.committeeEvents/maxEvents)*100}%`;
  document.getElementById("general-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.generalEvents/maxEvents)*100}%`;
    
  document.getElementById("social-events").innerHTML = userMeetingsForCurrentSemester.socialEvents;
  document.getElementById("volunteering-events").innerHTML = userMeetingsForCurrentSemester.voluenteeringEvents;
  document.getElementById("committee-events").innerHTML = userMeetingsForCurrentSemester.committeeEvents;
  document.getElementById("general-events").innerHTML = userMeetingsForCurrentSemester.generalEvents;

  document.getElementById("total-social-events").innerHTML = allMeetingsForCurrentSemester.socialEvents;
  document.getElementById("total-volunteering-events").innerHTML = allMeetingsForCurrentSemester.voluenteeringEvents;
  document.getElementById("total-committee-events").innerHTML = allMeetingsForCurrentSemester.committeeEvents;
  document.getElementById("total-general-events").innerHTML = allMeetingsForCurrentSemester.generalEvents;
  
}

const getStudentPoints = (endpointData) => {

  let studentData = endpointData[0];
  let allMeetingData = endpointData[1];

  // Trim down list to current semester only
  // console.log(endpointData)
  let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
  let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);

  let userMeetingsForCurrentSemester = getMeetingData(attendance);
  let allMeetingsForCurrentSemester = getMeetingData(listOfAllMeetings);

  // // Calculate total meetings of user
  // attendance.forEach(attendanceDay =>{
  //   switch (attendanceDay.meeting_type){
  //     case "SOCIAL":
  //       socialEvents += 1;
  //       break;
  //     case "VOLUNTEER":
  //       voluenteeringEvents +=1;
  //       break;
  //     case "COMMITTEE":
  //       committeeEvents +=1;
  //       break;
  //     case "GENERAL":
  //       generalEvents +=1;
  //       break;
  //     default:
  //       otherEvents +=1;
  //   }
  // });

  // // Calculate total meetings per category
  // listOfAllMeetings.forEach(meeting =>{
  //   switch (meeting.meeting_type){
  //     case "SOCIAL":
  //       allSocialEvents += 1;
  //       break;
  //     case "VOLUNTEER":
  //       allVoluenteeringEvents +=1;
  //       break;
  //     case "COMMITTEE":
  //       allCommitteeEvents +=1;
  //       break;
  //     case "GENERAL":
  //       allGeneralEvents +=1;
  //       break;
  //     default:
  //       allOtherEvents +=1;
  //   }
  // });

  showResults(userMeetingsForCurrentSemester, allMeetingsForCurrentSemester);

  // Draw bars and display numbers.
  // document.getElementById("social-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.socialEvents/maxEvents)*100}%`;
  // document.getElementById("volunteering-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.voluenteeringEvents/maxEvents)*100}%`;
  // document.getElementById("committee-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.committeeEvents/maxEvents)*100}%`;
  // document.getElementById("general-total-points-bar").style.width = `${(userMeetingsForCurrentSemester.generalEvents/maxEvents)*100}%`;
    
  // document.getElementById("social-events").innerHTML = userMeetingsForCurrentSemester.socialEvents;
  // document.getElementById("volunteering-events").innerHTML = userMeetingsForCurrentSemester.voluenteeringEvents;
  // document.getElementById("committee-events").innerHTML = userMeetingsForCurrentSemester.committeeEvents;
  // document.getElementById("general-events").innerHTML = userMeetingsForCurrentSemester.generalEvents;

  // document.getElementById("total-social-events").innerHTML = allMeetingsForCurrentSemester.socialEvents;
  // document.getElementById("total-volunteering-events").innerHTML = allMeetingsForCurrentSemester.voluenteeringEvents;
  // document.getElementById("total-committee-events").innerHTML = allMeetingsForCurrentSemester.committeeEvents;
  // document.getElementById("total-general-events").innerHTML = allMeetingsForCurrentSemester.generalEvents;
}


// getProfile().then(
//   getStudentPoints
// );
// console.log("Loaded profile");

// const loadSemesters = () => {
//   const container = document.getElementById("semestersContainer");
//   container.innerHTML = "";

//   semesters_wics.forEach(sem => {
//       const semElement = document.createElement("div");
//       semElement.innerHTML = 
//       `<h3>${sem.semester_wics} ${sem.year_wics}</h3>` +
//       `<p>${sem.organizer_wics}, ${sem.meeting_type_wics}: ${sem.description_wics}, ${sem.point_value_wics}</p>`;
//       container.appendChild(semElement);
//     }
//   );
// };
