<?php $thisPage="Log"; ?>
  <!DOCTYPE html>
  <html>

  <head>
    <?php include_once("head.php"); ?>
  </head>
  <body>
    <div id="main">
      <?php include_once("header.php"); ?>
      <?php include_once("menu.php"); ?>
        <table id="activity-table" class="content"><tr>
               <th><span class="flaticon-calendar"</span></th>
               <th><span class="flaticon-clock-1"</span></th>
               <th><span class="flaticon-stopwatch-1"</span></th>
               <th><span class="flaticon-star"</span></th>
          <?php
	    class MyDB extends SQLite3
	    {
    	      function __construct()
    	      {
                $this->open('/var/www/databases/barkActivity.db',SQLITE3_OPEN_READONLY);
              }
            }

	    $db = new MyDB();
            $html = "";
	    $result = $db->query('SELECT * FROM sessions ORDER BY datetime DESC');
            while(($row = $result->fetchArray())){
              $timestamp = $row['datetime'];
              //$date = date("D, d M", $timestamp);
              //$time = date("h:i:s A", $datetime);
              $datetime = new DateTime("@".$timestamp);
              $datetime->setTimezone(new DateTimeZone('America/New_York'));
              $time = $datetime->format("h:i:s A");
              $date = $datetime->format("D, d M");
              $duration = number_format($row['duration'],0,"",",");
              $duration = ($duration > 60) ? gmdate("i:s",$duration) : gmdate(":s",$duration);
              $reward = "";
              if($row['rewarded']) $reward = '<span>&#10004;</span>';
              $html .= "<tr><td>".$date."</td><td>".$time."</td><td>".$duration."</td><td>".$reward."</td></tr>";
	    }
            echo $html;
            $db->close();
          ?>
        </table>
    </div>
    <?php include_once("footer.php"); ?>
  </body>
</html>


