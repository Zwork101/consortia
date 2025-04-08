let minPointRequirements = 0;

//Enum for attendance
const AttendancePercentage = Object.freeze({
  Percent100: 3,
  Percent75: 2,
  Percent50: 1,
})

//const hasMentorshipPoints = 3;
const endpointOrganizationID = 2;

/**
 * Given a number of hours, return a number of points
 * @param {Number} hours The number of hours one has volunteered
 * @param {Array} volunteerRules An array of objects with the rules of how to award points.
 * @returns The number of points to be awarded
 */
function getVolunteeringPoints(hours, volunteer){
  for (volunteerParameter of volunteer) {
    if (hours >= volunteerParameter.threshold){
      return volunteerParameter.points;
    }
  }
  return 0;
}

/**
 * The amount of attendance points one would earn.
 * @param {Number} attendedMeetings The number of meetings the user has atteneded
 * @param {Number} totalMeetings The total number of meetings that has existed in the semester
 * @param {Array} attendanceRules An array of objects with the rules of how to award points.
 * @returns A number of points based on the percentage
 */
function getAttendancePoints(attendedMeetings, totalMeetings, attendanceRules){
  let meetingAttendedPercentage = (attendedMeetings/totalMeetings)*100;
  console.log(meetingAttendedPercentage);

  for (attendanceParameter of attendanceRules) {
    if (meetingAttendedPercentage >= attendanceParameter.percent){
      return attendanceParameter.points;
    }
  }
}

/**
 * Create an Object that contains values of points
 * @param {Array} listOfUserMeetings The list of meetings for this semester
 * @param {Array} listOfAllMeetings The list of all meetings for this semester 
 * @param {Object} pointConfig An object containing point configuration data.
 * @param {Number} bonusPoints The number of bonus points to award.
 * @returns An Object containg values of points
 */
function getPointObject(listOfUserMeetings, pointConfig, bonusPoints){
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

  listOfUserMeetings.forEach(attendanceDay =>{
    if (attendanceDay.meeting_type == "GENERAL"){
      attendedMeetings += 1;
    } else if (attendanceDay.meeting_type == "VOLUNTEER"){
      volunteeringHours += attendanceDay.hours; 
    } else if (attendanceDay.meeting_type == "MENTORSHIP"){
      mentorshipPoints += 1;
    }
  })
  if (mentorshipPoints > 0){
    mentorshipPoints += pointConfig.mentorship_minimum;
  }

  mentorshipPoints = Math.min(mentorshipPoints, pointConfig.mentorship_maximum);
  volunteeringPoints = getVolunteeringPoints(volunteeringHours, pointConfig.volunteer);
  attendancePoints = getAttendancePoints(attendedMeetings, totalMeetings, pointConfig.attendance);
  miscPoints = bonusPoints;

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
 * @param {Object} pointsFromThisSemester An object with point values from the most recent 
 * @returns The minimum point requirements.
 */
function showResults(pointsFromThisSemester, pointConfig){
  let earnedPoints = pointSummer(pointsFromThisSemester);
  minPointRequirements = pointConfig.required_points;

  /*
   * Points explainer (the gray boxes on the bottom)
   */
  // Mentorship
  document.getElementById("joined-program-points").innerHTML = minPointRequirements;

  // Volunteer
  for (volunteerParameter of pointConfig.volunteer) {
    var volunteerElement = `
                  <div>
                    <p>${volunteerParameter.threshold}+ Hours</p>
                    <p>${volunteerParameter.points} Points</p>
                  </div>`
    //console.log(volunteerElement);
    document.getElementById("volunteering-points-box").insertAdjacentHTML('afterbegin' , volunteerElement);
    
  }
  document.getElementById("volunteering-points-box").insertAdjacentHTML('afterbegin' , `<h2>Volunteering</h2>`);

  // Attendance
  for (attendanceParameter of pointConfig.attendance) {
    var attendanceElement = `
                <div>
                    <p>${attendanceParameter.percent}% of Meetings Attended</p>
                    <p>${attendanceParameter.points} Points</p>
                </div>`
    document.getElementById("attendance-points-box").insertAdjacentHTML('afterbegin' , attendanceElement);
  }
  document.getElementById("attendance-points-box").insertAdjacentHTML('afterbegin' , `<h2>Attendance</h2>`);

  /*
   * Progress Bar 
   */

  document.getElementById("mentor-points").innerHTML= pointsFromThisSemester.mentorshipPoints;
  document.getElementById("voluenteering-points").innerHTML= pointsFromThisSemester.volunteeringPoints;
  document.getElementById("attendance-points").innerHTML= pointsFromThisSemester.attendancePoints;
  document.getElementById("misc-points").innerHTML= pointsFromThisSemester.miscPoints;
    
  document.getElementById("earned-points").innerHTML= earnedPoints;
  document.getElementById("min-point-requirement").innerHTML= minPointRequirements;

  // If the user exceeds the max events, we want to resize the bar so that it does not cause UI conflicts.
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
  
  return minPointRequirements;
}

/**
 * Process the data for COMS.
 * @param {Object} studentData An Object representing the data of a student.
 * @param {Object} allMeetingData An Object that represents the data of all meetings.
 * @param {Object} settingsAndConfigData An object containing all the settings and configuration data
 */
function processDataCOMS(studentData, allMeetingData, settingsAndConfigData){

  let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
  let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);

  let pointsFromThisSemester = getPointObject(attendance, settingsAndConfigData.config, studentData.profile.bonus_points);

  showResults(pointsFromThisSemester, settingsAndConfigData.config);

  historyBuilder(builderMode.COMS, studentData, allMeetingData, settingsAndConfigData);
}