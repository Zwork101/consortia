let maxEvents = 14;

let socialEvents = 0;
let voluenteeringEvents = 0;
let committeeEvents = 0;
let generalEvents = 0;
let otherEvents = 0;

const getProfile = async () => {
	const endpoint = "http://localhost:8080/profile/1?org_id=1";
	try {
    	const response = await fetch(endpoint);
	    if (!response.ok) {
	      throw new Error(`Response status: ${response.status}`);
	    }

	    const json = await response.json();
	    // console.log(json);
      return json
	 } catch (error) {
	    console.error(error.message);
  }
}

const getStudentPoints = (studentData) => {
	//table = document.getElementById("orgMembers");

  console.log(studentData)
  // console.log(studentData.profile.attendance)

  let attendance = studentData.profile.attendance;
  // attendance.forEach(attendanceDay =>{
  //   //console.log(attendanceDay)
  //   //console.log(attendanceDay.meeting_type)
  //   if (attendanceDay.meeting_type == "GENERAL"){
  //     generalEventsEvents += 1;
  //     // console.log(mentorshipPoints);
  //   }
  // })

  attendance.forEach(attendanceDay =>{
    console.log("Type: "+attendanceDay.meeting_type)
    switch (attendanceDay.meeting_type){
      case "SOCIAL":
        socialEvents += 1;
        console.log("SE "+socialEvents);
        break;
      case "VOLUNTEER":
        voluenteeringEvents +=1
        console.log("VE "+voluenteeringEvents);
        break;
      case "COMMITTEE":
        committeeEvents +=1
        console.log("CE "+committeeEvents);
        break;
      case "GENERAL":
        generalEvents +=1
        console.log("GE "+generalEvents);
        break;
      default:
        otherEvents +=1
        console.log("Other Events "+otherEvents);
    }
  });
  
  document.getElementById("social-total-points-bar").style.width = `${(socialEvents/maxEvents)*100}%`;
  document.getElementById("volunteering-total-points-bar").style.width = `${(voluenteeringEvents/maxEvents)*100}%`;
  document.getElementById("committee-total-points-bar").style.width = `${(committeeEvents/maxEvents)*100}%`;
  document.getElementById("general-total-points-bar").style.width = `${(generalEvents/maxEvents)*100}%`;
    
    // document.getElementById("mentor-points").innerHTML= mentorshipPoints;
    // document.getElementById("voluenteering-points").innerHTML= voluenteeringid="general-total-points-bar"Points;
    // document.getElementById("attendence-points").innerHTML= attendencePoints;
    // document.getElementById("misc-points").innerHTML= miscPoints;
    
    // earnedPoints = mentorshipPoints + voluenteeringPoints + attendencePoints + miscPoints;
    document.getElementById("social-events").innerHTML = socialEvents;
    document.getElementById("volunteering-events").innerHTML = voluenteeringEvents;
    document.getElementById("committee-events").innerHTML = committeeEvents;
    document.getElementById("general-events").innerHTML = generalEvents;
}


getProfile().then(
  getStudentPoints
)
