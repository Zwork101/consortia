const getProfile = async () => {
    	const profileEndpoint = `/profile?org=${endpointOrganizationID}`;
      const meetingsEndpoint = `/meetings/${endpointOrganizationID}`;
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


getProfile().then(
  getStudentPoints
)