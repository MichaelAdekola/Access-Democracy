////////////////////////////////////////////

// Global vars

var _pastBillsDataByDebateID = {};

////////////////////////////////////////////
////////////////////////////////////////////
////////////////////////////////////////////

async function initiateDebateList(topicName = "")
{
	var startTime = getCurrTime();
	
	var outer = document.getElementById('inner_box2_id');
	
	newHTML = "";
	
	newHTML += `<div class="center">`;
	newHTML += "<h2>" + ("Loading...").toUpperCase() + "</h2>";
	newHTML += `</div>`;
	
	newHTML += `<div class="center" id="displayPcnt_debates">`;
	newHTML += `</div>`;
	
	//newHTML += `<div class="center" id="debateDataPcnt">`;
	//newHTML += `</div>`;
	
	newHTML += `<div class="center">`;
	newHTML += `<img src="loadingIconC" alt="loadingImage" class="loadingImage">`;
	newHTML += `</div>`;
	
	outer.innerHTML = newHTML;
	
	var displayPcntElem = document.getElementById('displayPcnt_debates');
	var voteDataPcntElem = document.getElementById('debateDataPcnt');
	
	//await fetch('/api/getBillsWithTopic_getAll_withoutAyesAndNoes/' + topicName).then(function (response) // Currently just used to get the bill IDs
	//await fetch('/api/getBillsBWithTopic_getAll_withoutAyesAndNoes/' + topicName).then(function (response)
	await fetch('/api/getBillsBWithTopic_statusBeforeRepsOrSen/' + topicName).then(function (response)
	{
		response.json().then(async function (json)
		{
			var debateData = []; 
			json.map(function(row) { debateData.push(row); });
			
			displayPcntElem.innerHTML = "<h3>" + ("Debates found relating to " + topicName + ": ").toUpperCase() + debateData.length.toString() + "</h3>";
			
			var data = [];
			
			if (debateData.length > 0)
			{
				populateDebateList(debateData, topicName);
			}
			else
			{
				newHTML = "";
				
				newHTML += `<div class="center">`;
				newHTML += "<h2>" + ("No debates relating to specified topic").toUpperCase() + "</h2>";
				newHTML += `</div>`;
				
				outer.innerHTML = newHTML;
			}
			
		});
	});
	
	
	
	
}

async function populateDebateList(debateData, topicName)
{
	var startTime = getCurrTime();
	
	var outer = document.getElementById('inner_box2_id');
	
	newHTML = "";
	
	newHTML += `<div class="center">`;
	newHTML += "<h2>" + ("Debates relating to " + topicName).toUpperCase() + "</h2>";
	newHTML += `</div>`;
	
	//newHTML += `<div class="debateBox">`;
	//newHTML += `</div>`;
	
	for (var i = 0; i < debateData.length; ++i)
	{
		
		newHTML += `<div class="debateBox_outer">`;
			
			newHTML += `<div class="debateBox">`;
			
				//var splStr = debateData[i][1].split(":");
				//var billNameText = splStr[2];
				//billNameText = billNameText.replace(/[^a-z0-9 .,;:]/gi,' '); // Remove any strange characters
				
				var billNameText = debateData[i][1];
				
				var billNameText_cut = billNameText.substring(0, 40) + "...";
				
				//newHTML += `<p class="debateBoxTitleText" title="` + billNameText + `"><a href="` + debateData[i][4] + `" style="color:rgb(255,255,255)">` + billNameText_cut + `</a></p>`;
				newHTML += `<p class="debateBoxTitleText" title="` + billNameText + `" onclick="openBillB(` + debateData[i][0] + `)">` + billNameText_cut + `</p>`;
				
				//
				
				//var billDescText = debateData[i][7];
				//billDescText = billDescText.replace(/[^a-z0-9 .,;:]/gi,' '); // Remove any strange characters
				
				var billDescText = debateData[i][10];
				
				newHTML += `<p class="descText">` + billDescText; // debateData[i][1];
				newHTML += `</p>`;
				
			newHTML += `</div>`;
			
		newHTML += `</div>`;
		
	}
	
	
	
	
	
	
	outer.innerHTML = newHTML;
}
































