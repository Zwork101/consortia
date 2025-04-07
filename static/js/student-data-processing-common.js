const organizationID = Object.freeze({
    WIC: 1,
	COMS: 2,
})

const getProfile = async () => {
    const profileEndpoint = `/profile?org=${endpointOrganizationID}`;
    const meetingsEndpoint = `/meetings/${endpointOrganizationID}`;
	const settingsEndpoint = `/settings/${endpointOrganizationID}`;
	try {
		var endpointList = []
		const profileResponse = await fetch(profileEndpoint);
		if (!profileResponse.ok) {
			throw new Error(`Response status: ${profileResponse.status}`);
		}

		const profileJson = await profileResponse.json();
		endpointList.push(profileJson);

		const meetingsResponse = await fetch(meetingsEndpoint);
		if (!meetingsResponse.ok) {
			throw new Error(`Response status: ${meetingsResponse.status}`);
		}

		const meetingsJson = await meetingsResponse.json();
		endpointList.push(meetingsJson);

		const settingsResponse = await fetch(settingsEndpoint);
		if (!settingsResponse.ok) {
			throw new Error(`Response status: ${settingsResponse.status}`);
		}

		const settingsJson = await settingsResponse.json();
		endpointList.push(settingsJson);
		
		return endpointList;
	} catch (error) {
		console.error(error.message);
	}
}

const getStudentPoints = (endpointData) => {

	let studentData = endpointData[0];
	let allMeetingData = endpointData[1];
	let settingsData = endpointData[2];

	if (endpointOrganizationID == organizationID.WIC){
		processDataWIC(studentData, allMeetingData, settingsData);
	} else if (endpointOrganizationID == organizationID.COMS){
		processDataCOMS(studentData, allMeetingData);
	} else {
		console.log("Invalid Endpoint");
	}
}

getProfile().then(
  getStudentPoints
)