let maxPoints = 0;
let earnedPoints = 0;

// For attendence
let attendedMeetings = 0;
let totalMeetings = 0; 

// Calculate points for the user
let mentorshipPoints = 0;
let voluenteeringPoints = 0;
let attendancePoints = 0;
let miscPoints = 0;

// Calculate total points that can be picked in total:
let totalVolunteerPoints = 0;

//Enum for attendance
const AttendancePercentage = Object.freeze({
  Percent100: 3,
  Percent75: 2,
  Percent50: 1,
})

const hasMentorshipPoints = 3;

const getProfile = async () => {
	const profileEndpoint = "http://localhost:8080/profile/1?org_id=1";
  const meetingsEndpoint = "http://localhost:8080/meetings";
	try {
      var endpointList = []
    	const response = await fetch(profileEndpoint);
	    if (!response.ok) {
	      throw new Error(`Response status: ${response.status}`);
	    }

	    const json = await response.json();
      endpointList.push(json);

	    const response2 = await fetch(meetingsEndpoint);
	    if (!response2.ok) {
	      throw new Error(`Response status: ${response2.status}`);
	    }

	    const json2 = await response2.json();
      endpointList.push(json2);
      
      return endpointList;
	 } catch (error) {
	    console.error(error.message);
  }
}



const getStudentPoints = (endpointData) => {

  studentData = endpointData[0];
  allMeetingData = endpointData[1];

  // Calculate points fo the user
  if (studentData.profile.membership == true){
    mentorshipPoints += hasMentorshipPoints;
  } 
  let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
  attendance.forEach(attendanceDay =>{
    if (attendanceDay.meeting_type == "GENERAL"){
      attendedMeetings += 1;
    } else if (attendanceDay.meeting_type == "VOLUNTEER"){
      voluenteeringPoints += attendanceDay.point_value; 
    } else if (attendanceDay.meeting_type == "MENTORSHIP"){
      // TODO
    }
  })

  miscPoints = studentData.profile.bonus_points;

  //Calculate max number of points
  let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);
  listOfAllMeetings.forEach(meeting => {
    if (meeting.meeting_type == "GENERAL"){
      totalMeetings += 1;
    } else if (meeting.meeting_type == "VOLUNTEER") {
      totalVolunteerPoints += meeting.point_value
    } else if (meeting.meeting_type == "MENTORSHIP"){
      // TODO
    }
  })

  let meetingAttendedPercentage = attendedMeetings/totalMeetings;

  if (meetingAttendedPercentage == 1){
    attendancePoints = AttendancePercentage.Percent100;
  } else if (meetingAttendedPercentage >= .75){
    attendancePoints = AttendancePercentage.Percent75;
  } else if (meetingAttendedPercentage >= .5){
    attendancePoints = AttendancePercentage.Percent50;
  }

  // Point rewarding

  earnedPoints = mentorshipPoints + voluenteeringPoints + attendancePoints + miscPoints;
  maxPoints = hasMentorshipPoints + totalVolunteerPoints + AttendancePercentage.Percent100 + miscPoints;

  document.getElementById("mentor-bar").style.width = `${(mentorshipPoints/maxPoints)*100}%`;
  document.getElementById("voluenteer-bar").style.width = `${(voluenteeringPoints/maxPoints)*100}%`;
  document.getElementById("attendance-bar").style.width = `${(attendancePoints/maxPoints)*100}%`;
  document.getElementById("misc-bar").style.width = `${(miscPoints/maxPoints)*100}%`;
    
  document.getElementById("mentor-points").innerHTML= mentorshipPoints;
  document.getElementById("voluenteering-points").innerHTML= voluenteeringPoints;
  document.getElementById("attendance-points").innerHTML= attendancePoints;
  document.getElementById("misc-points").innerHTML= miscPoints;
    
  document.getElementById("earned-points").innerHTML= earnedPoints;
  document.getElementById("max-points").innerHTML= maxPoints;
}

getProfile().then(
  getStudentPoints
)

const loadSemesters = () => {
  const container = document.getElementById("semesters");

  semesters.forEach(sem => {
      const semElement = document.createElement("div");
      semElement.innerHTML = 
      '<h3>${sem.semester_coms} ${sem.year_coms}</h3>' +
      '<p>{sem.organizer_coms}, ${sem.meeting_type_coms}: ${sem.description_coms}, ${sem.point_value_coms}</p>';
      container.appendChild(semElement);
    }
  );
};