let maxPoints = 18;
let earnedPoints = 0;

// For volunteering 
// let volunteeringHours = 0;
// let totalVolunteerHours = 0;

// // For attendence
// let attendedMeetings = 0;
// let totalMeetings = 0; 

// // Calculate points for the user
// let mentorshipPoints = 0;
// let volunteeringPoints = 0;
// let attendancePoints = 0;
// let miscPoints = 0;

// Calculate total points that can be picked in total:
let totalMentorshipPoints = 0;
let totalVolunteerPoints = 0;

//Enum for attendance
const AttendancePercentage = Object.freeze({
  Percent100: 3,
  Percent75: 2,
  Percent50: 1,
})

const hasMentorshipPoints = 3;

const endpointOrganizationID = 2;

// const getProfile = async () => {
// 	const profileEndpoint = "/profile?org=2";
//   const meetingsEndpoint = "/meetings/2";
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
 * Given a number of hours, return a number of points
 * @param {Number} hours The number of hours one has volunteered
 * @returns The number of points to be awarded
 */
function getVolunteeringPoints(hours){
  if (hours > 9){
    return 4;
  } else if (hours > 6){
    return 3;
  } else if (hours > 3){
    return 2;
  } else if (hours > 1){
    return 1;
  } else {
    return 0;
  }
}

/**
 * The amount of attendance points one would earn.
 * @param {*} attendedMeetings The number of meetings the user has atteneded
 * @param {*} totalMeetings The total number of meetings that has existed in the semester
 * @returns 0-4 points based on the percentage
 */
function getAttendancePoints(attendedMeetings, totalMeetings){
  let meetingAttendedPercentage = attendedMeetings/totalMeetings;

  if (meetingAttendedPercentage == 1){
    return AttendancePercentage.Percent100;
  } else if (meetingAttendedPercentage >= .75){
    return AttendancePercentage.Percent75;
  } else if (meetingAttendedPercentage >= .5){
    return AttendancePercentage.Percent50;
  } else {
    return 0;
  }
}

/**
 * Create an Object that contains values of points
 * @param {Array} listOfmeetings The list of meetings
 * @returns An Object containg values of points
 */
function getPointObject(listOfmeetings){
  let pointObject = {};

  let volunteeringHours = 0;

  // For attendence
  let attendedMeetings = 0;
  let totalMeetings = 0; 

  // Calculate points for the user
  let mentorshipPoints = 0;
  let volunteeringPoints = 0;
  let attendancePoints = 0;
  let miscPoints = 0;

  listOfmeetings.forEach(attendanceDay =>{
    if (attendanceDay.meeting_type == "GENERAL"){
      attendedMeetings += 1;
    } else if (attendanceDay.meeting_type == "VOLUNTEER"){
      volunteeringHours += attendanceDay.hours; 
    } else if (attendanceDay.meeting_type == "MENTORSHIP"){
      mentorshipPoints += 1;
    }
  })
  if (mentorshipPoints > 0){
    mentorshipPoints += hasMentorshipPoints;
  }

  mentorshipPoints = Math.min(mentorshipPoints, 9);
  volunteeringPoints = getVolunteeringPoints(volunteeringHours);
  attendancePoints = getAttendancePoints(attendedMeetings, totalMeetings);
  miscPoints = studentData.profile.bonus_points;

  pointObject.mentorshipPoints = mentorshipPoints;
  pointObject.volunteeringPoints = volunteeringPoints;
  pointObject.attendancePoints = attendancePoints;
  pointObject.miscPoints = miscPoints;

  console.log("aaa");
  console.log(pointObject);

  return pointObject;
}

/**
 * Display values for the bar on the "Current Semester" tab
 * @param {Object} pointsFromThisSemester An object with point values from the most recent semester
 */
function showResults(pointsFromThisSemester){
  earnedPoints = pointsFromThisSemester.mentorshipPoints + pointsFromThisSemester.volunteeringPoints + 
  pointsFromThisSemester.attendancePoints + pointsFromThisSemester.miscPoints;
  //maxPoints = totalMentorshipPoints + totalVolunteerPoints + AttendancePercentage.Percent100 + miscPoints;

  document.getElementById("mentor-points").innerHTML= pointsFromThisSemester.mentorshipPoints;
  document.getElementById("voluenteering-points").innerHTML= pointsFromThisSemester.volunteeringPoints;
  document.getElementById("attendance-points").innerHTML= pointsFromThisSemester.attendancePoints;
  document.getElementById("misc-points").innerHTML= pointsFromThisSemester.miscPoints;
    
  document.getElementById("earned-points").innerHTML= earnedPoints;
  document.getElementById("max-points").innerHTML= maxPoints;

  // If the user exceeds the max points, we want to resize the bar so that it does not cause UI conflicts.
  let pointUIValue;
  if (earnedPoints > maxPoints) {
    pointUIValue = earnedPoints;
  } else {
    pointUIValue = maxPoints;
  }
  document.getElementById("mentor-bar").style.width = `${(pointsFromThisSemester.mentorshipPoints/pointUIValue)*100}%`;
  document.getElementById("voluenteer-bar").style.width = `${(pointsFromThisSemester.volunteeringPoints/pointUIValue)*100}%`;
  document.getElementById("attendance-bar").style.width = `${(pointsFromThisSemester.attendancePoints/pointUIValue)*100}%`;
  document.getElementById("misc-bar").style.width = `${(pointsFromThisSemester.miscPoints/pointUIValue)*100}%`;
  
}

const getStudentPoints = (endpointData) => {

  studentData = endpointData[0];
  allMeetingData = endpointData[1];

  let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
  let pointsFromThisSemester = getPointObject(attendance);
  // attendance.forEach(attendanceDay =>{
  //   if (attendanceDay.meeting_type == "GENERAL"){
  //     attendedMeetings += 1;
  //   } else if (attendanceDay.meeting_type == "VOLUNTEER"){
  //     volunteeringHours += attendanceDay.hours; 
  //   } else if (attendanceDay.meeting_type == "MENTORSHIP"){
  //     mentorshipPoints += 1;
  //   }
  // })
  // if (mentorshipPoints > 0){
  //   mentorshipPoints += hasMentorshipPoints;
  // }
  // mentorshipPoints = Math.min(mentorshipPoints, 9);

  // volunteeringPoints = getVolunteeringPoints(volunteeringHours);
  // miscPoints = studentData.profile.bonus_points;


  //Calculate max number of points
  // let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);
  // listOfAllMeetings.forEach(meeting => {
  //   if (meeting.meeting_type == "GENERAL"){
  //     totalMeetings += 1;
  //   }
  // })

  // totalVolunteerPoints = getVolunteeringPoints(totalVolunteerHours);

  // attendancePoints = getAttendancePoints(attendedMeetings, totalMeetings);
  // let meetingAttendedPercentage = attendedMeetings/totalMeetings;

  // if (meetingAttendedPercentage == 1){
  //   attendancePoints = AttendancePercentage.Percent100;
  // } else if (meetingAttendedPercentage >= .75){
  //   attendancePoints = AttendancePercentage.Percent75;
  // } else if (meetingAttendedPercentage >= .5){
  //   attendancePoints = AttendancePercentage.Percent50;
  // }

  // Point rewarding

  showResults(pointsFromThisSemester);

  // earnedPoints = pointsFromThisSemester.mentorshipPoints + pointsFromThisSemester.volunteeringPoints + 
  //   pointsFromThisSemester.attendancePoints + pointsFromThisSemester.miscPoints;
  // //maxPoints = totalMentorshipPoints + totalVolunteerPoints + AttendancePercentage.Percent100 + miscPoints;

  // document.getElementById("mentor-points").innerHTML= pointsFromThisSemester.mentorshipPoints;
  // document.getElementById("voluenteering-points").innerHTML= pointsFromThisSemester.volunteeringPoints;
  // document.getElementById("attendance-points").innerHTML= pointsFromThisSemester.attendancePoints;
  // document.getElementById("misc-points").innerHTML= pointsFromThisSemester.miscPoints;
    
  // document.getElementById("earned-points").innerHTML= earnedPoints;
  // document.getElementById("max-points").innerHTML= maxPoints;

  // // If the user exceeds the max points, we want to resize the bar so that it does not cause UI conflicts.
  // let pointUIValue;
  // if (earnedPoints > maxPoints) {
  //   pointUIValue = earnedPoints;
  // } else {
  //   pointUIValue = maxPoints;
  // }
  // document.getElementById("mentor-bar").style.width = `${(pointsFromThisSemester.mentorshipPoints/pointUIValue)*100}%`;
  // document.getElementById("voluenteer-bar").style.width = `${(pointsFromThisSemester.volunteeringPoints/pointUIValue)*100}%`;
  // document.getElementById("attendance-bar").style.width = `${(pointsFromThisSemester.attendancePoints/pointUIValue)*100}%`;
  // document.getElementById("misc-bar").style.width = `${(pointsFromThisSemester.miscPoints/pointUIValue)*100}%`;

  historyBuilder(builderMode.COMS, studentData, allMeetingData);
}

// getProfile().then(
//   getStudentPoints
// )

const loadSemesters = () => {
  const container = document.getElementById("semesters");

  semesters.forEach(sem => {
      const semElement = document.createElement("div");
      semElement.innerHTML = 
      `<h3>${sem.semester_coms} ${sem.year_coms}</h3>` +
      `<p>${sem.organizer_coms}, ${sem.meeting_type_coms}: ${sem.description_coms}, ${sem.point_value_coms}</p>`;
      container.appendChild(semElement);
    }
  );
};