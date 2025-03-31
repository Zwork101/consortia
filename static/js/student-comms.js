let minPointRequirements = 18;

//Enum for attendance
const AttendancePercentage = Object.freeze({
  Percent100: 3,
  Percent75: 2,
  Percent50: 1,
})

const hasMentorshipPoints = 3;
const endpointOrganizationID = 2;

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
 * @param {Number} attendedMeetings The number of meetings the user has atteneded
 * @param {Number} totalMeetings The total number of meetings that has existed in the semester
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

  return pointObject;
}

/**
 * Sums all of the points together
 * @param {Object} pointObject Object containing all of the point values
 * @returns A number representing the total number of points earned.
 */
function pointSummer(pointObject){
  return pointObject.mentorshipPoints + pointObject.volunteeringPoints + 
  pointObject.attendancePoints + pointObject.miscPoints;
}

/**
 * Display values for the bar on the "Current Semester" tab
 * @param {Object} pointsFromThisSemester An object with point values from the most recent semester
 */
function showResults(pointsFromThisSemester){
  let earnedPoints = pointSummer(pointsFromThisSemester);

  document.getElementById("mentor-points").innerHTML= pointsFromThisSemester.mentorshipPoints;
  document.getElementById("voluenteering-points").innerHTML= pointsFromThisSemester.volunteeringPoints;
  document.getElementById("attendance-points").innerHTML= pointsFromThisSemester.attendancePoints;
  document.getElementById("misc-points").innerHTML= pointsFromThisSemester.miscPoints;
    
  document.getElementById("earned-points").innerHTML= earnedPoints;
  document.getElementById("min-point-requirement").innerHTML= minPointRequirements;

  // If the user exceeds the max points, we want to resize the bar so that it does not cause UI conflicts.
  let pointUIValue;
  if (earnedPoints > minPointRequirements) {
    pointUIValue = earnedPoints;
  } else {
    pointUIValue = minPointRequirements;
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

  showResults(pointsFromThisSemester);

  historyBuilder(builderMode.COMS, studentData, allMeetingData);
}