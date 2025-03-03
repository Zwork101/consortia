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

  let attendance = studentData.profile.attendance
  let mentorshipMeetingCount = 0
  let voluenteeringCount = 0
  let attendenceCount = 0
  let miscCount = 0

  attendance.forEach(attendanceDay =>{
    console.log(attendanceDay)
  })
    
}


getProfile().then(
  getStudentPoints
)
