
  <!DOCTYPE html>
  <html>

  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Actvity Log</title>
    <?php include_once("head.php"); ?>
  </head>
  <body>
    <div id="main">
      <div id="header">
        <img src="/img/header_logo.png" alt="TreatTrainer Logo"/>
      
	<span id="title">
            Activity Log
        </span>
      </div>
      <div id="content">
        <?php
	class MyDB extends SQLite3
	{
    	  function __construct()
    	  {
            $this->open('/var/www/databases/barkActivity.db',SQLITE3_OPEN_READONLY);
          }
        }

	$db = new MyDB();

	$result = $db->query('SELECT * FROM sessions ORDER BY duration, btime');
	$row = $result->fetchArray();
        var_dump($row);	
	?>
        </div>
      </div>
    </div>
    <?php include_once("footer.php"); ?>
  </body>
</html>


