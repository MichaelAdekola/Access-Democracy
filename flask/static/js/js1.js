////////////////////////////////////////////

// Global vars

var _bAwaitingSync = false;
var _lastSelectedListItem = null;
var _selectedMPID = -1;

var _mpImages = {};
var _pastBillsDataByBillID = {};

var _storedTime = 0.0;

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

function getCurrTime()
{
	var d = new Date();
	return d.getTime();
}

async function importMPImages()
{
	await fetch('/api/getMPImages').then(function (response)
	{
		response.json().then(function (json)
		{
			json.map(function(row) // Like a foreach loop
			{
				
				_mpImages[row[0]] = row[1];
				
			});
			
			console.log("importMPImages() complete");
			
			//console.log(_mpImages[0]);
			
			/* for (var key in _mpImages) 
			{
				console.log(key + " : " + _mpImages[key]);
				break;
			} */
			
		});
	});
}

async function initialiseTopicList(selectedTopic = null, searchTerm = "")
{
	_bAwaitingSync = true;
	
	//
	
	var listBox = document.getElementById('mainListBox');
	if (listBox)
	{
		
		await fetch('/api/getTopics').then(function (response)
		{
			// Will likely finish after the outer function does
			
			response.json().then(function (json)
			{
				
				var newHTML = "";
				
				newHTML += jsonToTopicTree(json, selectedTopic, searchTerm);
				
				listBox.innerHTML = newHTML;
				
				//
				
				activateTreeTogglers();
				
				setUpTreeLinks(json);
				
				
			});
		});
		
	}
	
	//activateTreeTogglers();
	
	populateBillToMainBox(171); // TEST - 22-9-20
	
	_bAwaitingSync = false;
}

async function activateTreeTogglers()
{
	var toggler = document.getElementsByClassName("caret");
	for (var i = 0; i < toggler.length; ++i)
	{
		toggler[i].addEventListener("click", function(event) 
		{
			//console.log(event.target.value);		
			if (event.currentTarget !== event.target) return; // Only fire when we click the actual item, not its children
			
			this.parentElement.querySelector(".nested").classList.toggle("active");
			this.classList.toggle("caret-down");
		});
	}
	
	//
	
	for (i = 0; i < toggler.length; i++) // Automatically open it them all at the beginning
	{			
		toggler[i].dispatchEvent(new Event('click'));
	}
}

function jsonToTable(json, tableNameStr)
{
	if (json[0] == null) return null;

	var cols = Object.keys(json[0]); // The result here should contain 2 items if using the Alpha, Bravo etc. database
	//var cols = Object.keys(json); // The result here would contain 6 items "" "" ""
	var headerRow = '';
	var bodyRows = '';

	cols.map(function (col) // Behaves like a foreach loop (with 'col' as the current var per itr)
	{
		headerRow += '<th>' + col + '</th>';
	});

	json.map(function (row)
	{
		bodyRows += '<tr>';

		cols.map(function (colName)
		{
			bodyRows += '<td>' + row[colName] + '</td>';
		});

		bodyRows += '</tr>';
	});

	var result = '<table id="' + tableNameStr + '"><thead><tr>' + headerRow + '</tr></thead><tbody>' + bodyRows + '</tbody></table>';
	//console.log(result);
	return result;
}

function jsonToTopicTree(json, selectedTopic = null, searchTerm = "")
{
	if (json[0] == null) return null;
	
	var listRows = "";
		
	listRows += `<ul id="myUL">`;
	
	json.map(function(row) // Like a foreach loop
	{
		
		//var searchTerm = "";
		
		searchTerm = searchTerm.toLowerCase();
		
		var bParentHasSearchTerm = false;
		var bAChildHasSearchTerm = false;
		
		if (searchTerm == "")
		{
			bParentHasSearchTerm = true;
			bAChildHasSearchTerm = true;
		}
		
		bParentHasSearchTerm = row[1] == "" && (searchTerm == "" || row[0].toLowerCase().includes(searchTerm));
		
		// If the search term is found in one of row's children, the parent must also be allowed to exist
		
		//if (searchTerm == "" || ( row[0].toLowerCase().includes(searchTerm) || row[1].toLowerCase().includes(searchTerm) ))
		//if (searchTerm == "" || ( row[0].toLowerCase().includes(searchTerm) || row[1].toLowerCase().includes(searchTerm) ))
		
		//console.log("row[0]: " + row[0]);
		
		var childRows = "";
		json.map(function(rowInner)
		{
			if (rowInner[1] == row[0]) // We are a child of the current row
			{
				var bvB = rowInner[0];

				if (bParentHasSearchTerm || searchTerm == "" || bvB.toLowerCase().includes(searchTerm))
				{
					bAChildHasSearchTerm = true;
					
					var className = "li_istB";
					
					//if (selectedTopic != null && bvB == selectedTopic) className = "li_istB_selected"; // Works

					childRows += `<li><span class="` + className + `">` + bvB + `</span></li>`;
				}
			}
		});
		
		var caretClass = "caret";
		if (childRows.length == 0) caretClass = "caret-invisible";
		
		if (row[1] == "") // We're a parent
		{
			var bv = row[0];
			
			//if (bParentHasSearchTerm || bAChildHasSearchTerm || searchTerm == "" || bv.toLowerCase().includes(searchTerm))
			if (bParentHasSearchTerm || bAChildHasSearchTerm)
			{
				listRows += `<li><span class="` + caretClass + `"><span class="li_ist">` + bv +`</span></span>`;
			}
		}
		
		if (childRows.length > 0)
		{
			listRows += `<ul class="nested">`;
			listRows += childRows;
			listRows += `</ul>`;
		}
		
	});
	
	listRows += `</ul>`;
	
	return listRows;
}

async function setUpTreeLinks(json) // Sets up event for populating inner boxes 1 and 2
{
	var elements = [];
	elements = elements.concat([].slice.call(document.getElementsByClassName("li_istB"))); // Convert result to an array
	elements = elements.concat([].slice.call(document.getElementsByClassName("li_istB_selected")));
	elements = elements.concat([].slice.call(document.getElementsByClassName("li_ist")));
	elements = elements.concat([].slice.call(document.getElementsByClassName("li_ist_selected")));
		
	for (var i = 0; i < elements.length; ++i)
	{
		elements[i].addEventListener("click", function(event)
		{
			/* if (event.currentTarget !== event.target) return; */
			
			/* console.log(this.classList); */
			
			if (_lastSelectedListItem != null)
			{
				if (_lastSelectedListItem.classList.contains("li_istB_selected"))
				{
					_lastSelectedListItem.classList.remove('li_istB_selected');
					_lastSelectedListItem.classList.add('li_istB');
				}
				
				if (_lastSelectedListItem.classList.contains("li_ist_selected"))
				{
					_lastSelectedListItem.classList.remove('li_ist_selected');
					_lastSelectedListItem.classList.add('li_ist');
				}
			}
			_lastSelectedListItem = this;
			
			if (this.classList.contains("li_istB"))
			{
				this.classList.remove('li_istB');
				this.classList.add('li_istB_selected');
			}
			
			if (this.classList.contains("li_ist"))
			{
				this.classList.remove('li_ist');
				this.classList.add('li_ist_selected');
			}
			
			//
			//
			
			//main_box_id
			
			var main_box = document.getElementById('main_box_id');
			
			var newHTML = "";
			
			//
			
			newHTML += `<div class="inner_box1" id="inner_box1_id">`;
					
				//newHTML += `<div class="center">`;
					//newHTML += `<h2>Select a topic to begin...</h2>`;
				//newHTML += `</div>`;
				
			newHTML += `</div>`;
			
			newHTML += `<div class="inner_box2" id="inner_box2_id">`;
			newHTML += `</div>`;
			
			newHTML += `<a id="viewChangeBtn_1" class="viewChangeBtn" onclick="onViewChangeButton_1_Clicked()">Scroll View</a>`;
			newHTML += `<a id="viewChangeBtn_2" class="viewChangeBtn" onclick="onViewChangeButton_2_Clicked()">Grid View</a>`;
			
			newHTML += `<div class="inner_box3" id="inner_box3_id">`;
			newHTML += `</div>`;
			
			//
			
			main_box.innerHTML = newHTML;
			
			//
			//
			
			var inner_box1 = document.getElementById('inner_box1_id');
			
			newHTML = "";
			
			var topicName = this.parentElement.textContent;
			
			console.log(topicName);
			
			newHTML += `<div class="center">`;
				newHTML += "<h1>" + topicName.toUpperCase() + "</h1>";
			newHTML += `</div>`;
			
			// TODO: Get contents of topics db 
			
			//
			
			var ourRow = null;
			
			json.map(function(row) // Like a foreach loop
			{
				//console.log(row);
				
				//if (row[2] === topicName)
				if (row[0] === topicName)
				{
					ourRow = row;
				}
			});
			
			//
			
			//newHTML += `<div class="center">`;
			//newHTML += ourRow[2]; // Description text
			//newHTML += `</div>`;
			
			//
			
			inner_box1.innerHTML = newHTML;
			
			//
			//
			
			//inner_box2
			
			/* var inner_box2 = document.getElementById('inner_box2_id');
			
			newHTML = "";
			
			newHTML += `<div class="center">`;
			newHTML += "<h2>" + ("Upcoming votes and debates").toUpperCase() + "</h2>";
			newHTML += `</div>`;
			
			newHTML += `<div class="center">`;
			newHTML += "<p>TODO: Add list of votes/debates related to the selected topic here -- both past and future<\p>";
			newHTML += `</div>`;
			
			
			inner_box2.innerHTML = newHTML; */
			
			//
			
			initiateDebateList(topicName);
			
			//
			
			initiateVoteList(topicName);
			
		});
	}
}


async function populateBillToMainBox(billIdx, lastViewedTopic = "")
{
	console.log("populateBillToMainBox: " + billIdx.toString())
	
	var main_box = document.getElementById('main_box_id');
	
	main_box.innerHTML = "";
		
	//
	
	// TODO: Get all 'bills' which are actually just copies of this one bill (if possible)
	// TODO: Also create new WS script to get the bill-stage data - such as: https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Search_Results/Result?bId=r6536
	// TODO: Add a 'back' button in the top left corner which takes the user back to the previous 'topic' view that they were looking at -- will need to pass the topic in when populating this
	
	await fetch('/api/getBillBByID/' + billIdx).then(function (response)
	{
		response.json().then(async function (json)
		{
			
			var newHTML = "";
			
			//
			
			console.log(json);
			
			newHTML += `<div class="center">`;
				newHTML += `<h1>`;
					newHTML += "BILL";
				newHTML += `</h1>`;
			newHTML += `</div>`;
			
			
			newHTML += `<div class="billDisplay_inner_box" id="billDisplay_inner_box_ID">`;
			
				newHTML += `<div class="center">`;
				
					newHTML += `<h2 class="descLink"><a href="` + json[0][19] + `" style="color:rgb(255,255,255)">` + json[0][1] + `</a></h2>`;
					
					// newHTML += `<h2>`;
						// newHTML += json[0][1];
					// newHTML += `</h2>`;
					
				newHTML += `</div>`;
				
				newHTML += `<br>`;
				
				newHTML += `<div class="billDisplay_descBox">`;
					newHTML += `<p>`;
						
						newHTML += json[0][10];
						
					newHTML += `</p>`;
				newHTML += `</div>`;
				
				//
				
				newHTML += `<div class="billDisplay_descBoxB">`;
					
					newHTML += `<p>` + "Bill Type: " + json[0][4] + `</p>`;
					if (json[0][5] != "") newHTML += `<p>` + "Sponsors: " + json[0][5] + `</p>`;
					if (json[0][6] != "") newHTML += `<p>` + "Portfolio: " + json[0][6] + `</p>`;
					newHTML += `<p>` + "Originating House: " + json[0][7] + `</p>`;
					newHTML += `<p>` + "Status: " + json[0][8] + `</p>`;
					newHTML += `<p>` + "Parliament No: " + json[0][9] + `</p>`;
					
				newHTML += `</div>`;
				
				//
				
				newHTML += `<div class="billDisplay_graphContainer">`;
					
					//
					//
					
					// TL, BL, BR, TR
					//newHTML += `<polygon points="0,0 0,100 100,100 100,0" />`;
					
					//var polyArrow1 = `<polygon points="20,20 20,60     0,60 50,100 100,60     80,60 80,20" />`;
					var polyArrow1 = `<polygon points="25,20 25,60     0,60 50,100 100,60     75,60 75,20" />`;
					
					//var largeConnector1 = `<polygon points="49,14 49,86 51,86 51,14" />`;
					var largeConnector1 = `<polygon points="49,14   49,84 46,84 46,86   49,86 51,86   51,16 53,16  53,17  55,15  53,13  53,14   51,14" />`;
					
					//
					//
					
					// House of reps
					
					newHTML += `<h3 id="billDisplay_title_1">House of Representatives</h3>`;
					
					newHTML += `<div class="` + (json[0][11].includes("Introduced and read a first time") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_1" title="1st Reading">`;
						newHTML += `<p>1st Reading</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_1">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][11].includes("Second reading agreed to") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_2" title="2nd Reading">`;
						newHTML += `<p>2nd Reading</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_2">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="billDisplay_graphBox" id="billDisplay_graph_3" title="House Committee">`;
						newHTML += `<p>House Committee</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_3">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][11].includes("Consideration in detail debate") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_4" title="Consideration In Detail">`;
						newHTML += `<p>Consideration In Detail</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_4">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][11].includes("Third reading agreed to") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_5" title="3rd Reading">`;
						newHTML += `<p>3rd Reading</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_5">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + ((json[0][15] == "1" && json[0][11].includes("Third reading agreed to")) ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_6" title="Bill Passed (Reps)">`;
						newHTML += `<p>Bill Passed (Reps)</p>`;
					newHTML += `</div>`;
					
					// Senate
					
					newHTML += `<svg viewBox="0 0 100 100" class="largeConnectorSVG" id="largeConnectorSVG_1">`;
						newHTML += largeConnector1;
					newHTML += `</svg>`;
					
					
					
					newHTML += `<h3 id="billDisplay_title_2">Senate</h3>`;
					
					newHTML += `<div class="` + (json[0][13].includes("Introduced and read a first time") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_7" title="1st Reading">`;
						newHTML += `<p>1st Reading</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_7">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][13].includes("Second reading agreed to") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_8" title="2nd Reading">`;
						newHTML += `<p>2nd Reading</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_8">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="billDisplay_graphBox" id="billDisplay_graph_9" title="Senate Committee">`;
						newHTML += `<p>Senate Committee</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_9">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="billDisplay_graphBox" id="billDisplay_graph_10" title="Committee Of The Whole">`;
						newHTML += `<p>Committee Of The Whole</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_10">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][13].includes("Third reading agreed to") ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_11" title="3rd Reading">`;
						newHTML += `<p>3rd Reading</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_11">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][16] == "1" ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_12" title="Bill Passed (Sen)">`;
						newHTML += `<p>Bill Passed (Sen)</p>`;
					newHTML += `</div>`;
					
					// Governor General
					
					newHTML += `<svg viewBox="0 0 100 100" class="largeConnectorSVG" id="largeConnectorSVG_2">`;
						newHTML += largeConnector1;
					newHTML += `</svg>`;
					
					
					
					newHTML += `<h3 id="billDisplay_title_3">Governor-General</h3>`;
					
					newHTML += `<div class="` + (json[0][18] == "1" ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_13" title="Royal Assent - The Governor-General signs the bill">`;
						newHTML += `<p>Royal Assent</p>`;
					newHTML += `</div>`;
					
					newHTML += `<svg viewBox="0 0 100 100" class="downArrowSVG" id="downArrowSVG_13">`;
						newHTML += polyArrow1;
					newHTML += `</svg>`;
					
					
					newHTML += `<div class="` + (json[0][8] == "Act" ? "billDisplay_graphBox_yes" : "billDisplay_graphBox" ) + `" id="billDisplay_graph_14" title="Bill is an act of Parliament">`;
						newHTML += `<p>Bill Is Act Of Parliament</p>`;
					newHTML += `</div>`;
					
					//
					
				newHTML += `</div>`;
			
			newHTML += `</div>`;
			
			newHTML += `<a id="reportBtnID` + (1).toString() + `" class="reportBtn" onclick="onReportBtnClicked(` + (1).toString() + "," + billIdx.toString() + `)">Report as inaccurate</a>`;
			
			//
			
			main_box.innerHTML = newHTML;
			
		});
		
	});
	
}



//
//
//
//

async function populateMPList()
{
	await fetch('/api/getMPs').then(function (response)
	{
		response.json().then(async function (json)
		{
			
			var startTime = getCurrTime();
			
			//testBox2.innerHTML = jsonToTable(json, "main_box_table");
			
			var mpList = document.getElementById('mpList');
			
			var newHTML = "";
			
			if (mpList != null)
			{
				
				json.map(function(row) // Like a foreach loop
				{
					
					newHTML += `<option id="mpOption">`;
					
					//FName, SName, Electorate, PCode, StateAcronym
					//newHTML += row[4] + " " + row[3] + ", " + row[8] + ", " + row[18] + ", " + row[9];
					newHTML += row[4] + " " + row[5] + ", " + row[7] + ", " + row[8];
					
					newHTML += `</option>`;
					
				});
				
			}
			
			mpList.innerHTML = newHTML;
			
			document.getElementById('mpListInput').disabled = false;
			onMPListInputChanged(); // So it starts blinking
			
			console.log("populateMPList() completed in: " + ((getCurrTime() - startTime) * 0.001).toString() + " sec");
			
		});
	});
}

async function onMPListInputChanged()
{
	var mpListInput = document.getElementById('mpListInput');
	
	var val = mpListInput.value;
	
	console.log(val);
	
	var mpInput = document.getElementById('mpInputID');
	
	if (val == "" && !mpInput.classList.contains("mpInput_blinking") && !mpInput.disabled)
	{
		mpInput.classList.add("mpInput_blinking");
	}
	else if (mpInput.classList.contains("mpInput_blinking"))
	{
		mpInput.classList.remove("mpInput_blinking");
	}
}

async function onSearchFieldButtonClicked()
{
	var searchFieldInput = document.getElementById('searchField');
	
	var val = searchFieldInput.value;
	
	initialiseTopicList(selectedTopic = null, searchTerm = val);
}

async function onMPListButtonClicked()
{
	var mpListInput = document.getElementById('mpListInput');
	
	var val = mpListInput.value;
	//var test = mpListInput.selectedIndex;
	
	//var strUser = mpListInput.options[mpListInput.selectedIndex].value;
	
	//alert("onMPListButtonClicked A(): " + val);
	
	//var e = document.getElementById("mpListInput");
	//var strUser = e.options[e.selectedIndex].value;
	
	//alert("onMPListButtonClicked(): " + strUser);
		
	await fetch('/api/getMPByDetails/' + val).then(function (response)
	{
		response.json().then(async function (json)
		{
			
			json.map(function(row) // Like a foreach loop // Should only be one row here
			{
				//alert("onMPListButtonClicked B(): " + row);
				
				document.getElementById("mp_profile_image_main").src = row[2];
				
				var outer = document.getElementById('mpDisplay_right');
				
				newHTML = "";
				
				newHTML += `<p>`;
				newHTML += row[3] + " " + row[4] + " " + row[5];
				newHTML += `</p>`;
				
				newHTML += `<p>`;
				newHTML += "Electorate: " + row[7];
				newHTML += `</p>`;
				
				newHTML += `<p>`;
				newHTML += "Party: " + row[10];
				newHTML += `</p>`;
				
				newHTML += `<p>`;
				newHTML += "State: " + row[8];
				newHTML += `</p>`;
				
				if (row[9] != "")
				{
					newHTML += `<p>`;
					newHTML += "Title(s): " + row[9];
					newHTML += `</p>`;
				}
				
				mailIconIDs = ["mpContactIcon_A", "mpContactIcon_B", "mpContactIcon_C"]
				mailIconIDIdx = 0
				
				if (row[11].trim() != "")
				{
					newHTML += `<a href="` + row[11].trim() + `"><img title="Contact via Twitter" src="twitter.ico" alt="icon" class="mpContactIcon" id="` + mailIconIDs[mailIconIDIdx] + `"></a>`;
					mailIconIDIdx += 1
				}
				
				if (row[12].trim() != "")
				{
					newHTML += `<a href="` + row[12].trim() + `"><img title="Contact via Facebook" src="facebook.ico" alt="icon" class="mpContactIcon" id="` + mailIconIDs[mailIconIDIdx] + `"></a>`;
					mailIconIDIdx += 1
				}
				
				if (row[13].trim() != "")
				{
					newHTML += `<a href="` + "mailto:" + row[13].trim() + `"><img title="Contact via Email" src="email.ico" alt="icon" class="mpContactIcon" id="` + mailIconIDs[mailIconIDIdx] + `"></a>`;
				}
				
				outer.innerHTML = newHTML;
				
				//
				
				_selectedMPID = row[0]; // row[11]
				console.log("_selectedMPID: " + _selectedMPID.toString());
			});
			
		});
	});
	
}

function setMainDescContent()
{
	var mainDesc = document.getElementById('mainDesc');
	
	var mainDescContent = "";
	
	mainDescContent += "Satisfaction with democracy in Australia fell from 85.6% in 2007 to 40.56% in 2018.";
	mainDescContent += "<br>";
	mainDescContent += "<br>";
	mainDescContent += "As Australia is a representative democracy, politicians should be voting on behalf of their constituents, however, there is a strong sense among voters that this no longer happens and that politicians act in their own and in large corporations’ interests.";
	mainDescContent += "<br>";
	mainDescContent += "<br>";
	mainDescContent += "As voters disengage with politics, the only outcome is that the state of politics and our trust in it, continues to decline, which is already seeing dangerous consequences around the world, in the rise of authoritarianism.";
	mainDescContent += "<br>";
	mainDescContent += "<br>";
	mainDescContent += "In Australia, we have a chance to reverse this trend.  It is a huge task but the first step is for citizens to become informed about what is being voted on in our name within our democratic processes.  At the moment, information such as which issues are decided by Federal and which by State Parliaments, what bills are going to be/have been introduced and debated in Parliament, and how each MP has voted on these is extremely difficult and time consuming to track down and so it is understandable that most voters do not invest the time, but we have a right to have this information accessible to us in a  digestible format, and we need it to inform our vote.";
	
	mainDesc.innerHTML = mainDescContent;
}

function sendEmail()
{
    window.location.href = `mailto:mail@example.org? &subject=The%20subject%20of%20the%20mail &body=Hi, I found this website and thought you might like it`;
}

//
//
//
//

async function openBillB(billB_ID)
{
	populateBillToMainBox(billB_ID);
}

async function onReportBtnClicked(billIdx, billID)
{
	btn = document.getElementById('reportBtnID' + billIdx.toString());
	
	
	
	//console.log("onReportBtnClicked - billID:" + billID.toString());
	
	await fetch("/api/submitToBillReportCount",
	{
		method: 'POST',
		//body: JSON.stringify({ item: itemsListIdx, quantity: quantityListValue}),
		body: JSON.stringify({ item: billID }),
		headers: new Headers({ "content-type": "application/json" })
	}).then(function (response)
	{
		btn.style.pointerEvents = 'none';
		btn.text = "Reported";
		btn.classList.remove('reportBtn');
		btn.classList.add('reportBtn_inactive');
	});
}

async function onNextBtnClicked()
{
	slider = document.getElementById('sliderID');
	/* console.log(slider.offsetWidth); */
	slider.scrollBy(
	{
		left: 301,
		behavior: 'smooth' 
	});
}

async function onPrevBtnClicked()
{
	slider = document.getElementById('sliderID');
	slider.scrollBy(
	{
		left: -301,
		behavior: 'smooth' 
	});
}

//
//

async function setNoBillsText(outer)
{
	newHTML = "";
						
	newHTML += `<div class="center">`;
	newHTML += "<h2>" + ("No votes relating to specified topic").toUpperCase() + "</h2>";
	newHTML += `</div>`;
		
	outer.innerHTML = newHTML;
}

async function initiateVoteList(topicName = "")
{
	//console.log("_pastBillsDataByBillID.length: " + Object.keys(_pastBillsDataByBillID).length.toString());

	var startTime = getCurrTime();
	
	_storedTime = getCurrTime();
	
	var outer = document.getElementById('inner_box3_id');
	
	newHTML = "";
	
	newHTML += `<div class="center">`;
	newHTML += "<h2>" + ("Loading...").toUpperCase() + "</h2>";
	newHTML += `</div>`;
	
	newHTML += `<div class="center" id="displayPcnt">`;
	newHTML += `</div>`;
	
	newHTML += `<div class="center" id="billDataPcnt">`;
	newHTML += `</div>`;
	
	newHTML += `<div class="center">`;
	newHTML += `<img src="loadingIconC" alt="loadingImage" class="loadingImage">`;
	newHTML += `</div>`;
		
	outer.innerHTML = newHTML;
	
	var billDataPcntElem = document.getElementById('billDataPcnt');
	var displayPcntElem = document.getElementById('displayPcnt');
	
	// First, we need to find the indices of all bill items which are about our topic
	// Then we need to run await fetch('/api/getPastBillsData/x for each one and store the results (or draw the data from its stored place in the dictionary - 8-9-20)
	// Once we have the data, we need to pipe it into populateSlidingVoteList()
		
	//await fetch('/api/getBillsWithTopic_getAll/' + topicName).then(function (response) // Currently just used to get the bill IDs
	
	//await fetch('/api/getBillsWithTopic_getAll_withAyesAndNoes/' + topicName).then(function (response) // Until 22-9-20 // This gets bill data from the original bills table so the ID it provides matches the ID in the data from getPastBillsData
	await fetch('/api/getBillsBWithTopic_getAll_withAyesAndNoes/' + topicName).then(function (response) // This gets the bills from the billsB table and picks a bill in the bills table with a matching name (that has votes) to get the ID for getPastBillsData, so more convoluted
	{
		response.json().then(async function (json)
		{
			var billData = []; 
			json.map(function(row) // Like a foreach loop
			{
				billData.push(row);
			});
			
			displayPcntElem.innerHTML = "<h3>" + ("Votes found relating to " + topicName + ": ").toUpperCase() + billData.length.toString() + "</h3>";
			
			//console.log("billData.length: " + billData.length.toString());
			
			var data = [];
			
			if (billData.length > 0)
			{
				
				
				
				for (var i = 0; i < billData.length; ++i)
				{
					//billID = billData[i][0]; // Until 22-9-20 when switched to billsB
					billID = billData[i][21];
					
					//console.log("billID: " + billID.toString());
					
					// Now we store loaded bill data in a dict - so we don't have to load it more than once per session
					if (billID in _pastBillsDataByBillID) // Here, we add one bill to data and then check the count
					{
						bill = _pastBillsDataByBillID[billID]; // Reference
						data.push(bill);
						
						checkForVoteDataComplete(i, data, billData, startTime, billDataPcntElem, billID, true, topicName);
					}
					else // Bill data hasn't been loaded yet for bill with billID. Here, we also add one bill to data and then check the count
					{
						// Nested await fetch -- this can be seriously problematic. The for loop is setting off a whole bunch of new async processes which finish in different orders depending on how much time they take, so contents of 'data' ends up in the wrong order!
						await fetch('/api/getPastBillsData/' + billID).then(function (response) // Uses the bill's ID // Get the vote data by MP for display
						{
							response.json().then(async function (json)
							{
								// Important: Can't use billID under here as it will probably have changed from where it was by the time we get our response
								
								var bill = [];
								json.map(function(row) // Like a foreach loop
								{
									bill.push(row);
								});
								
								billID_local = bill[0][0];
								
								data.push(bill);
								
								_pastBillsDataByBillID[billID_local] = bill;
								
								checkForVoteDataComplete(i, data, billData, startTime, billDataPcntElem, billID_local, false, topicName);
							});
						});
					}
				}
				
				
				
			}
			else
			{
				setNoBillsText(outer);
				
				//console.log("initiateVoteList completed in: " + ((getCurrTime() - startTime) * 0.001).toString() + " sec");
			}
			
		});
	});
	
}

function checkForVoteDataComplete(i, data, billData, startTime, billDataPcntElem, billID, bUsingDictStoredData, topicName)
{
	var billDataPcnt = Math.round(((i / billData.length) * 100)).toString() + "%";
	if (billDataPcntElem)
	{
		if (bUsingDictStoredData) billDataPcntElem.innerHTML = "<h3>" + ("Retrieving bill data... ").toUpperCase() + billDataPcnt + "</h3>";
		else billDataPcntElem.innerHTML = "<h3>" + ("Downloading bill data... ").toUpperCase() + billDataPcnt + "</h3>";
	}
	
	//console.log("data.length: " + data.length.toString());
	//console.log("billData.length: " + billData.length.toString());
	
	if (data.length == billData.length) // We have all of the data - now we can populate the list or grid
	{
		sortVoteDataAndPopulate(i, data, billData, topicName);
		//console.log("initiateVoteList completed in: " + ((getCurrTime() - startTime) * 0.001).toString() + " sec");
		
		return true;
	}
	
	return false;
}

function sortVoteDataAndPopulate(i, data, billData, topicName)
{
	//var billDataPcntElem = document.getElementById('billDataPcnt');
	
	var billDataSorted = [];
	var dataSorted = [];
	
	var bCanPopulate = false;
	
	//console.log("initiateVoteList up to sorting in: " + ((getCurrTime() - startTime) * 0.001).toString() + " sec");
	
	// Resort the data into the proper order
	
	//var test = 0;
	
	//console.log("data.length: " + data.length.toString());
	
	/* for (var i = 0; i < billData.length; ++i)
	{
		console.log("billData[i]: " + billData[i]);
	} */
	
	//console.log("sortVoteDataAndPopulate -- data.length: " + data.length.toString())
	//console.log("sortVoteDataAndPopulate -- billData.length: " + billData.length.toString())
	
	/* for (var i = 0; i < data.length; ++i)
	{
		console.log("data[i]: " + data[i][0]);
	} */
	
	while (dataSorted.length < data.length)
	{
		for (var j = 0; j < data.length; ++j)
		{
			//if (data[j][0][0] == billData[dataSorted.length][0])
			if (data[j][0][0] == billData[dataSorted.length][21]) // 22-9-20
			{
				//console.log("push");
				
				billDataSorted.push(billData[dataSorted.length]);
				dataSorted.push(data[j]);
				break;
			}
		}
		
		//++test;
		//console.log(test);
		//if (test > 50) break;
	}
	
	//
	
	//console.log("sortVoteDataAndPopulate -- dataSorted.length: " + dataSorted.length.toString())
	//console.log("sortVoteDataAndPopulate -- billDataSorted.length: " + billDataSorted.length.toString())
	
	//
	
	if (dataSorted.length == 0) setNoBillsText(outer);
	else
	{
		bCanPopulate = true;
	}
	
	//var billDataPcnt = Math.round(((i / billData.length) * 100)).toString() + "%";
	//if (billDataPcntElem) billDataPcntElem.innerHTML = "<h3>" + ("Bill data... ").toUpperCase() + billDataPcnt + "</h3>";
	
	//
	
	if (bCanPopulate)
	{
		populateSlidingVoteList(dataSorted, billDataSorted, topicName);
		//populateGridVoteList(data, billData); // TODO: Implement this
	}
}

async function populateSlidingVoteList(data, billData, topicName)
{
	var startTime = getCurrTime();
		
	//displayPcntElem.innerHTML = "<h3>" + ("Preparing display... ").toUpperCase() + "</h3>";
	//if (!displayPcntElem) console.log("ERROR: !displayPcntElem");
	
	// 3-9-20 -- If these are not the same length, we might have a problem
	//console.log("populateSlidingVoteList -- data.length: " + data.length.toString())
	//console.log("populateSlidingVoteList -- billData.length: " + billData.length.toString())
	if (data.length != billData.length) console.log("WARNING: populateSlidingVoteList -- data.length != billData.length")
	
	var outer = document.getElementById('inner_box3_id');
	
	//
	
	var newHTML = "";
	
	newHTML += `<div class="center">`;
	newHTML += "<h2>" + ("Votes relating to " + topicName).toUpperCase() + "</h2>";
	newHTML += `</div>`;
	
	newHTML += `<div class="wholeSlidingSectionHolder" id="wholeSlidingSectionHolderID">`;
		
		newHTML += `<div class="slidingSectionSide" id="slidingSectionSide_left" onclick="onPrevBtnClicked()">`;
			newHTML += `<img src="arrow_lft.png" alt="image" title="Aye" class="slidingSectionSideImg">`;
		newHTML += `</div>`;
		
		newHTML += `<div class="sliderHolder" id="sliderHolderID">`;
			newHTML += `<div class="slider" id="sliderID">`;
			
			for (var i = 0; i < data.length; ++i) // Number of bills
			{
				
				// Note: These could probably be retrieved from billData - 8-9-20
				var count_aye = 0;
				var count_nay = 0;
				for (var j = 0; j < data[i].length; ++j)
				{
					 if (data[i][j][6] == "aye") count_aye += 1;
					 if (data[i][j][6] == "nay") count_nay += 1;
				}
				
				//
				
				newHTML += `<div class="slide" id="slide-`;
				newHTML += data.length.toString();
				newHTML += `">`;
					
					newHTML += `<div class="slideInner" id="slideInner">`;
						
						var voteHeaderClass = "voteHeader";
						
						// Until 22-9-20
						//if (billData[i][5] > billData[i][6]) voteHeaderClass = "voteHeader_passed";
						//if (billData[i][5] < billData[i][6]) voteHeaderClass = "voteHeader_negatived";
						
						if (billData[i][22] > billData[i][23]) voteHeaderClass = "voteHeader_passed";
						if (billData[i][22] < billData[i][23]) voteHeaderClass = "voteHeader_negatived";
						
						newHTML += `<div id="voteHeader" class="` + voteHeaderClass + `">`;
						
						//
							
							// Until 22-9-20
							//var splStr = billData[i][1].split(":");
							//var billNameText = splStr[2];
							//billNameText = billNameText.replace(/[^a-z0-9 .,;:]/gi,' '); // Remove any strange characters
							
							var billNameText = billData[i][1];
							
							//newHTML += `<p class="descLink"><a href="` + billData[i][4] + `" style="color:rgb(255,255,255)">` + billNameText + `</a></p>`;
							newHTML += `<p class="descLink" onclick="openBillB(` + billData[i][0] + `)">` + billNameText + `</p>`;
							
							//
							
							// Until 22-9-20
							//var billDescText = billData[i][7];
							//billDescText = billDescText.replace(/[^a-z0-9 .,;:]/gi,' '); // Remove any strange characters
							
							var billDescText = billData[i][10];
							
							newHTML += `<p class="descText">` + billDescText; // billData[i][1];
							newHTML += `</p>`;
							
						//
						
						newHTML += `</div>`;
						
						//
						//

						var dictAyes = {};
						var dictNoes = {};
						
						for (var j = 0; j < data[i].length; ++j)
						{
							var ayeOrNay = data[i][j][6];
							var party = data[i][j][4];
							
							if (ayeOrNay == "aye")
							{								
								if (party in dictAyes) dictAyes[party] += 1;
								else dictAyes[party] = 1;
							}
							
							if (ayeOrNay == "nay")
							{
								if (party in dictNoes) dictNoes[party] += 1;
								else dictNoes[party] = 1;
							}
						}
												
						newHTML += `<div class="votesByParty" id="votesByParty">`;
						
							newHTML += `<div class="vbp_left">`;
								
								newHTML += `<div class="vbp_left_A">`;
									newHTML += `<img src="yes.ico" alt="image" title="Aye" class="vpbYesImage">`;
									newHTML += `<p class="vpbText vpbTextYes">` + "" + count_aye.toString() + `</p>`;
								newHTML += `</div>`;
								
								newHTML += `<div class="vbp_left_B">`;
									for (var key in dictAyes) 
									{
										newHTML += `<p class="descText">` + key + ": " + dictAyes[key] + `</p>`;
									}
								newHTML += `</div>`;
								
							newHTML += `</div>`;
							
							newHTML += `<div class="vbp_right">`;
								
								newHTML += `<div class="vbp_right_A">`;
									newHTML += `<img src="no.ico" alt="image" title="Nay" class="vpbNoImage">`;
									newHTML += `<p class="vpbText vpbTextNo">` + "" + count_nay.toString() + `</p>`;
								newHTML += `</div>`;
								
								newHTML += `<div class="vbp_right_B">`;
									for (var key in dictNoes) 
									{
										newHTML += `<p class="descText">` + key + ": " + dictNoes[key] + `</p>`;
									}
								newHTML += `</div>`;
								
							newHTML += `</div>`;
							
						newHTML += `</div>`;
						
						//
						
						newHTML += `<div class="tableHolder" id="tableHolder">`;
						
							newHTML += `<table>`;
							/* newHTML += `<caption>Insert caption</caption>`; */
							
							newHTML += 
								`
								<tr>
									<th>MP</th>
									<th>Name</th>
									<th>Party</th>
									<th>District</th>
									<th>Vote</th>
									<th>Contact</th>
								</tr>
								`;
							
							//
							
							//_selectedMPID
							
							data_local = data[i];
							
							//data_local_reordered = [];
							for (var j = 0; j < data_local.length; ++j)
							{
								if (data_local[j][10] == _selectedMPID)
								{
									temp = data_local[j];
									data_local.splice(j, 1);
									data_local.unshift(temp);
									break;
								}
							}
							//data_local = data_local_reordered;
							
							//
							
							//for (var j = 0; j < 25; ++j) // Number of entries per bill - should equate to the number of aye votes + the number of nay votes // (ayeCount + nayCount)
							for (var j = 0; j < data_local.length; ++j)
							{
								
								if (data_local[j][10] == _selectedMPID)
								{
									newHTML += `<tr id="selRow">`;
								}
								else
								{
									newHTML += `<tr>`;
								}
									
									newHTML += `<td>`;
										newHTML += `<div class="center">`;
										
											var imageSrc = "profile.ico";
											if (data_local[j][10] in _mpImages) imageSrc = _mpImages[data_local[j][10]];
										
											newHTML += `<img src="` + imageSrc + `" alt="mp_profile_image" class="tableCellProfileImage">`;
										
										newHTML += `</div>`;
									newHTML += `</td>`;
									
									newHTML += `<td>` + data_local[j][2] + " " + data_local[j][3] + `</td>`; // Scott Morrison
									newHTML += `<td>` + data_local[j][4] +`</td>`; // Liberal
									newHTML += `<td>` + data_local[j][5] +`</td>`; // Place
									
									if (data_local[j][6] == "aye")
									{
										newHTML += `<td>`;
											newHTML += `<div class="center">`;
												newHTML += `<img src="yes.ico" alt="image" title="Aye" class="yesImage">`;
											newHTML += `</div>`;
										newHTML += `</td>`
									 }
									 else
									 {
										 newHTML += `<td>`;
											newHTML += `<div class="center">`;
												newHTML += `<img src="no.ico" alt="image" title="Nay" class="noImage">`;
											newHTML += `</div>`;
										newHTML += `</td>`
									 }
									
									newHTML += `<td>`;
										newHTML += `<div class="center">`;
											
											if (data_local[j][7] != "")
												newHTML += `<a href="` + data_local[j][7] + `"><img title="Contact via Twitter" src="twitter.ico" alt="icon" class="tableCellEmailImage"></a>`;
											
											if (data_local[j][8] != "")
												newHTML += `<a href="` + data_local[j][8] + `"><img title="Contact via Facebook" src="facebook.ico" alt="icon" class="tableCellEmailImage"></a>`;
											
											if (data_local[j][9] != "")
												newHTML += `<a href="` + "mailto:" +data_local[j][9] + `"><img title="Contact via Email" src="email.ico" alt="icon" class="tableCellEmailImage"></a>`;
											
										newHTML += `</div>`;
									newHTML += `</td>`;
									
								newHTML += `</tr>`;
							}
							
							newHTML += `</table>`;
						
						newHTML += `</div>`;
					
					newHTML += `</div>`;
					
					//newHTML += `<a id="reportBtnID` + (i).toString() + `" class="reportBtn" onclick="onReportBtnClicked(` + (i).toString() + "," + (data[i][0][0]).toString() + `)">Report as inaccurate</a>`;
					newHTML += `<a id="reportBtnID` + (i).toString() + `" class="reportBtn" onclick="onReportBtnClicked(` + (i).toString() + "," + (billData[i][0]).toString() + `)">Report as inaccurate</a>`;
					
				newHTML += `</div>`;
				
				// Note: I believe that the HTML rendering is not being updated often enough for this to be functional
				//var displayPcnt = Math.round(((i / data.length) * 100)).toString() + "%";
				//if (displayPcntElem) displayPcntElem.innerHTML = "<h3>" + ("Visualisation... ").toUpperCase() + displayPcnt + "</h3>";
				
			}
			newHTML += `</div>`;
		newHTML += `</div>`;
		
		newHTML += `<div class="slidingSectionSide" id="slidingSectionSide_right" onclick="onNextBtnClicked()">`;
			newHTML += `<img src="arrow_rgt.png" alt="image" title="Aye" class="slidingSectionSideImg">`;
		newHTML += `</div>`;
		
	newHTML += `</div>`;
	
	outer.innerHTML = newHTML;
	
	//
	
	//console.log("populateSlidingVoteList completed in: " + ((getCurrTime() - startTime) * 0.001).toString() + " sec");
	console.log("all regarding vote sliding list completed in: " + ((getCurrTime() - _storedTime) * 0.001).toString() + " sec");
	
	return 0;
}

async function populateGridVoteList(data, billData) // TODO: Implement this
{
	
}

function init()
{
	setMainDescContent();
	populateMPList();
	initialiseTopicList();
	importMPImages();
}




window.onload = init;








































