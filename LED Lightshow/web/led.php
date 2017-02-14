<?php
	$type = $_GET["type"];
	
	switch($type){
		case "custCol":
			exec("sudo pkill python");
			exec("sudo python /home/pi/custCol.py ".$_GET["col"]);
			break;
		case "fade":
			exec("sudo pkill python");
			exec("sudo python /home/pi/fade.py ".$_GET["time"]);
			break;
		case "breathe":
			exec("sudo pkill python");
			exec("sudo python /home/pi/breathe.py ".$_GET["col"]." ".$_GET["time"]);
			break;
		case "rainbow":
			exec("sudo pkill python");
			exec("sudo python /home/pi/rainbow.py");
			break;
		case "flashR":
			exec("sudo pkill python");
			exec("sudo python /home/pi/flash.py r ".$_GET["time"]);
			break;
		case "flashC":
			exec("sudo pkill python");
			exec("sudo python /home/pi/flash.py c ".$_GET["time"]." ".$_GET["col"]);
			break;
		case "stop":
			exec("sudo pkill python");
			exec("sudo python /home/pi/stop.py");
	}
?>