let points = 0;
let maxPoints = 60;
let earnedPoints = 0;
let totalPoints = 0;

let mentorshipPoints = 0;
let voluenteeringPoints = 0;
let attendencePoints = 0;
let miscPoints = 0;

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

  // console.log(studentData)
  // console.log(studentData.profile.attendance)

  if (studentData.profile.membership == "active"){
    mentorshipPoints += 3
    // console.log(points)
  } 

  let attendance = studentData.profile.attendance
  attendance.forEach(attendanceDay =>{
    //console.log(attendanceDay)
    //console.log(attendanceDay.meeting_type)
    if (attendanceDay.meeting_type == "GENERAL"){
      mentorshipPoints += 1;
      // console.log(mentorshipPoints);
    } else if (attendanceDay.meeting_type == "VOLUNTEER"){
      voluenteeringPoints += attendanceDay.point_value; 
      // console.log("Vol Points: " + voluenteeringPoints);
    }

    miscPoints = studentData.profile.bonus_points;
  })


  // Point rewarding
    document.getElementById("mentor-bar").style.width = `${(mentorshipPoints/maxPoints)*100}%`;
    document.getElementById("voluenteer-bar").style.width = `${(voluenteeringPoints/maxPoints)*100}%`;
    document.getElementById("misc-bar").style.width = `${(miscPoints/maxPoints)*100}%`;
    
    document.getElementById("mentor-points").innerHTML= mentorshipPoints;
    document.getElementById("voluenteering-points").innerHTML= voluenteeringPoints;
    document.getElementById("attendence-points").innerHTML= attendencePoints;
    document.getElementById("misc-points").innerHTML= miscPoints;
    
    earnedPoints = mentorshipPoints + voluenteeringPoints + attendencePoints + miscPoints;
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