
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

        <div>
          <?php
	    $db = new SQLite3('/var/www/database/barkActivity.db');

	    $results = $db->query('SELECT bar FROM foo');
	    while ($row = $results->fetchArray()) {
    	      var_dump($row);
	    }

	  ?>
        </div>
      </div>
    </div>
    <?php include_once("footer.php"); ?>
  </body>
</html>


