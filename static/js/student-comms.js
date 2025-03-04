let points = 0
let maxPoints = 20
let mentorshipMeetingCount = 0
let voluenteeringCount = 0
let attendenceCount = 0
let miscCount = 0

const getProfile = async () => {
	const endpoint = "http://localhost:8080/profile/1?org_id=1";
	try {
    	const response = await fetch(endpoint);
	    if (!response.ok) {
	      throw new Error(`Response status: ${response.status}`);
	    }

	    const json = await response.json();
	    console.log(json);
      return json
	 } catch (error) {
	    console.error(error.message);
  }
}

const getStudentPoints = (studentData) => {
	//table = document.getElementById("orgMembers");

  console.log(studentData)
  console.log(studentData.profile.attendance)

  if (studentData.profile.membership == "active"){
    points += 3
    console.log(points)
  } 

  let attendance = studentData.profile.attendance
  attendance.forEach(attendanceDay =>{
    //console.log(attendanceDay)
    console.log(attendanceDay.meeting_type)
    if (attendanceDay.meeting_type == "GENERAL"){
      points += 1
      console.log(points)
    }
    document.getElementById("mentor-bar").style.width = `${(points/maxPoints)*100}%`
  })

    
}


getProfile().then(
  getStudentPoints
)
