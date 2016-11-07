<?php 
    $thisPage="Status"; 
    $name = "His Holiness the Pup";
?>
  <!DOCTYPE html>
  <html>

  <head>
    <?php include_once("head.php"); ?>
  </head>
  <body>
    <div id="main">
      <?php include_once("header.php"); ?>
      <?php include_once("menu.php"); ?>
      <h1>Current Status</h1>

      <?php $statusfile =fopen("status",'r');
            $status = fread($statusfile,filesize($statusfile));
            switch ($status) {
                case 0:
                    echo '<div class="status ok"><span class="flaticon-success icon"></span><span>'.$name.' has not been barking</span></div>';
                    break;
                case 1:
                    echo '<div class="status recent"><span class="flaticon-warning icon"></span><span>'.$name.' was barking recently</span></div>';
                    break;
                case 2:
                    echo '<div class="status barking"><span class="flaticon-warning icon"></span><span>'.$name.' is currently barking</span></div>';
                    break;
                default:
                    break;
            }
      ?>
      <div class="content">


        <p> 
        <?php
	    $Barkstop ='barkstop=True';
        class MyDB extends SQLite3
	    {
    	      function __construct()
    	      {
                $this->open('/var/www/databases/barkActivity.db',SQLITE3_OPEN_READONLY);
              }
            }

	    $db = new MyDB();
	    $result = $db->query('SELECT * FROM sessions ORDER BY datetime DESC LIMIT 1');
        $row = $result->fetchArray();
        $timestamp = $row['datetime'];
        $datetime = new DateTime("@".$timestamp);
        $datetime->setTimezone(new DateTimeZone('America/New_York'));
        $time = $datetime->format("h:i:s A");
        $date = $datetime->format("D, d M");
        $duration = number_format($row['duration'],0,"",",");
        $duration = ($duration > 60) ? gmdate("i:s",$duration) : gmdate(":s",$duration);
        $reward = "";
        if($row['rewarded']) $reward = '<span>&#10004;</span>';
        $status = "The last barking session was on ".$date." at ".$time.". It lasted for ".$duration.".";
        
        if($row['rewarded']) $status .= " The puppy was rewarded for quieting.";
        else{
	        $result = $db->query('SELECT datetime FROM sessions WHERE rewarded ORDER BY datetime DESC LIMIT 1');
            $row = $result->fetchArray();
            $timestamp = $row['datetime'];
            $datetime = new DateTime("@".$timestamp);
            $datetime->setTimezone(new DateTimeZone('America/New_York'));
            $time = $datetime->format("h:i:s A");
            $date = $datetime->format("D, d M");
            $status .= " The puppy's last reward was at ".$time." on ".$date.".";
        }
	    
        //Check if currently barking
            //run script that returns value of session
            //if session=true, create notification of active barking       

        //Check if barking was today
            //else, check last session date, if = today, create notification of recent barking
        $notification ="";
        date_default_timezone_set('America/New_Yotk');
        $today = date("D, d M");
        if($date == $today){
            $notification='<span id="notification-recent">His Holiness has been barking today!</span>';
        }

        $html = $notification.$status;
        echo $html



 
          ?>
        </p>
      </div>
    </div>
    <?php include_once("footer.php"); ?>
  </body>
</html>


