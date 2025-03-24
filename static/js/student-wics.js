let maxEvents = 14;

let socialEvents = 0;
let voluenteeringEvents = 0;
let committeeEvents = 0;
let generalEvents = 0;
let otherEvents = 0;

let allSocialEvents = 0;
let allVoluenteeringEvents = 0;
let allCommitteeEvents = 0;
let allGeneralEvents = 0;
let allOtherEvents = 0;

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

  let studentData = endpointData[0];
  let allMeetingData = endpointData[1];

  let attendance = getMeetingsFromThisSemester(studentData.profile.attendance);
  let listOfAllMeetings = getMeetingsFromThisSemester(allMeetingData.Meetings);

  attendance.forEach(attendanceDay =>{
    switch (attendanceDay.meeting_type){
      case "SOCIAL":
        socialEvents += 1;
        break;
      case "VOLUNTEER":
        voluenteeringEvents +=1
        break;
      case "COMMITTEE":
        committeeEvents +=1
        break;
      case "GENERAL":
        generalEvents +=1
        break;
      default:
        otherEvents +=1
    }
  });

  listOfAllMeetings.forEach(meeting =>{
    switch (meeting.meeting_type){
      case "SOCIAL":
        allSocialEvents += 1;
        break;
      case "VOLUNTEER":
        allVoluenteeringEvents +=1
        break;
      case "COMMITTEE":
        allCommitteeEvents +=1
        break;
      case "GENERAL":
        allGeneralEvents +=1
        break;
      default:
        allOtherEvents +=1
    }
  });
  
  document.getElementById("social-total-points-bar").style.width = `${(socialEvents/maxEvents)*100}%`;
  document.getElementById("volunteering-total-points-bar").style.width = `${(voluenteeringEvents/maxEvents)*100}%`;
  document.getElementById("committee-total-points-bar").style.width = `${(committeeEvents/maxEvents)*100}%`;
  document.getElementById("general-total-points-bar").style.width = `${(generalEvents/maxEvents)*100}%`;
    
    document.getElementById("social-events").innerHTML = socialEvents;
    document.getElementById("volunteering-events").innerHTML = voluenteeringEvents;
    document.getElementById("committee-events").innerHTML = committeeEvents;
    document.getElementById("general-events").innerHTML = generalEvents;

    document.getElementById("total-social-events").innerHTML = allSocialEvents;
    document.getElementById("total-volunteering-events").innerHTML = allVoluenteeringEvents;
    document.getElementById("total-committee-events").innerHTML = allCommitteeEvents;
    document.getElementById("total-general-events").innerHTML = allGeneralEvents;
}


getProfile().then(
  getStudentPoints
)


const loadSemesters = () => {
  const container = document.getElementById("semestersContainer");
  container.innerHTML = "";

  semesters_wics.forEach(sem => {
      const semElement = document.createElement("div");
      semElement.innerHTML = 
      '<h3>${sem.semester_wics} ${sem.year_wics}</h3>' +
      '<p>${sem.organizer_wics}, ${sem.meeting_type_wics}: ${sem.description_wics}, ${sem.point_value_wics}</p>';
      container.appendChild(semElement);
    }
  );
};
