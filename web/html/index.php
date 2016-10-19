<?php $thisPage="Status"; ?>
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
      <div class="content">
        <p> 
          <?php
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
            $datetime = strtotime($row['datetime']);
            $date = date("m/d/y", $datetime);
            $time = date("g:i A", $datetime);
            $duration = number_format($row['duration'],0,"",",");
            $html = "The last barking session was on ".$date." at ".$time." for ".$duration." seconds.";
            echo $html;
            if($row['rewarded']) $reward = " The puppy was rewarded for quieting.";
            else{
	        $datetime = $db->query('SELECT datetime FROM sessions WHERE rewarded ORDER BY datetime DESC LIMIT 1');
                $date = date("m/d/y", $datetime);
                $time = date("g:i A", $datetime);
                $reward = " The puppy's last reward was at ".$time." on ".$date.".";
            }
            echo $reward;
          ?>
        </p>
      </div>
    </div>
    <?php include_once("footer.php"); ?>
  </body>
</html>


