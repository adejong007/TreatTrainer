<?php $thisPage="Controller"; ?>
  <!DOCTYPE html>
  <html>

  <head>
    <?php include_once("head.php"); ?>
  </head>
  <body>
    <div id="main">
      <?php include_once("header.php"); ?>
      <?php include_once("menu.php"); ?>
      <h1>Controls</h1>

      <p id="message" class="status"></p>
      <div class="content">

        <div id="controls">
          <button id="start" class="control" type="button"><span class="flaticon-play-button-1"></span></button>
          <button id="stop"  class="control" type="button"><span class="flaticon-pause-1"></span></button>
          <button id="treat"  class="control" type="button"><span class="flaticon-star"></span></button>
        </div>

        <script type="text/javascript">
            $('#stop').click(function(){

              $.ajax({
                type: 'POST',
                url: 'stopDetection.php',
                success: function(data) {
                    $("#message").slideUp( "fast" );
                    $("#message").text('TreatTrainer has stopped');
                    $("#message").slideDown( "slow" );
                }
              });
            });
            $('#start').click(function(){

              $.ajax({
                type: 'POST',
                url: 'startDetection.php',
                success: function(data) {

                    $("#message").slideUp( "fast" );
                    $("#message").text('TreatTrainer is now running');
                    $("#message").slideDown( "slow" );

                }
              });
            });
            $('#treat').click(function(){

              $.ajax({
                type: 'POST',
                url: 'dropTreat.php',
                success: function(data) {
                    $("#message").slideUp( "fast" );
                    $("#message").text('A treat has been dropped');
                    $("#message").slideDown( "slow" );
                }
              });
            });
        </script>
      </div>
    </div>
    <?php include_once("footer.php"); ?>
  </body>
</html>


