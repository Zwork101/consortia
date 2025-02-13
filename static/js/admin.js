const listProfiles = async () => {
	const endpoint = "http://localhost:8080/admin/profiles/0";
	try {
    	const response = await fetch(endpoint);
	    if (!response.ok) {
	      throw new Error(`Response status: ${response.status}`);
	    }

	    const json = await response.json();
	    console.log(json);
	 } catch (error) {
	    console.error(error.message);
  }
}

const addTableRows = () => {
	table = document.getElementById("dbTable");
	
	var newElement = '<div id="two">two</div>'
	element.insertAdjacentHTML( 'afterend', newElement )
}

`
<tr class="dbTableRow">
            <td>
                <label class="container">
                    <input type="checkbox" >
                    <span class="checkmark"></span>
                </label>
            </td>
            <td>Will</td>
            <td>Smith</td>
            <td>non-active</td>
            <td>9 semesters</td>
            <td>wms6730@rit.edu</td>
            <td>0 Points</td>
            <td>1 Point</td>
            <td>4 Points</td>
            <td>3 Points</td>
            <td>8 Points</td>
            <td class="dbTablePH"></td>
            <td><img src="../static/images/options.png" width="16" /></td>
        </tr>
`
listProfiles();