function httpGet(url){
    var request = new XMLHttpRequest();
	request.open( "GET" , url, true);
	request.send(null);
}

function custCol(){
	var custColValue = document.getElementById("custColValue").value;
	while(custColValue.charAt(0) === "#")
		custColValue = custColValue.substr(1);
	console.log("COLOR " + custColValue);
	console.log("led.php?type=custCol&col="+custColValue);
	httpGet("led.php?type=custCol&col="+custColValue);
}

function fade(){
	var fadeLength = document.getElementById("fadeLength").value;

	console.log("I'M FADED!!!! " + fadeLength);
	httpGet("led.php?type=fade&time="+fadeLength);
}

function breath(){
	var breathCol = document.getElementById("breathCol").value;
	var breathLength = document.getElementById("breathLength").value;
	while(breathCol.charAt(0) === "#")
		breathCol = breathCol.substr(1);
	console.log("breathe into me and make me real! " + breathCol + " " + breathLength);
	httpGet("led.php?type=breathe&col="+breathCol+"&time="+breathLength);
}

document.getElementById("flashRandomCol").onchange = function() {
    document.getElementById("flashCol").disabled = this.checked;
};

function flash(){
	var flashCol = document.getElementById("flashCol").value;
	while(flashCol.charAt(0) === "#")
		flashCol = flashCol.substr(1);
	var flashLength = document.getElementById("flashLength").value;
	var flashRandomCol = document.getElementById("flashRandomCol").checked;
	if(flashRandomCol){
		console.log("It's seizure time :D " + flashLength);
		httpGet("led.php?type=flashR&time="+flashLength);
	} else {
		console.log("It's controlled seizure time :D " + flashLength + " " + flashCol);
		httpGet("led.php?type=flashC&time="+flashLength+"&col="+flashCol);
	}
}

function rainbow(){
	console.log("I can see a rainbow!");
	httpGet("led.php?type=rainbow");
}

function stopLed(){
	console.log("She cannae' take anymore capn'!");
	httpGet("led.php?type=stop");
}