const listProfiles = async () => {
	const endpoint = "http://localhost:8080/student/meetings/1";
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

const addTableRows = (rows) => {
	table = document.getElementById("orgMembers");

  rows.forEach(row => {
    var newElement = `
      <tr class="dbTableRow">
                  <td>
                      <label class="container">
                          <input type="checkbox" >
                          <span class="checkmark"></span>
                      </label>
                  </td>
                  <td>${row['profile']['first_name']}</td>
                  <td>${row['profile']['last_name']}</td>
                  <td>${row['profile']['membership']}</td>
                  <td>Undetermined</td>
                  <td>${row['profile']['email']}</td>
                  <td>Undetermined</td>
                  <td>Undetermined</td>
                  <td>Undetermined</td>
                  <td>Undetermined</td>
                  <td>${row['profile']['points']}</td>
                  <td class="dbTablePH"></td>
                  <td><img src="../static/images/options.png" width="16" /></td>
              </tr>
      `
    table.insertAdjacentHTML( 'beforeend', newElement )
  });
    
}


listProfiles().then(
  addTableRows
)
