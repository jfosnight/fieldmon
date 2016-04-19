<!DOCTYPE html>
<html>
	<head>
		<meta content="width=device-width,minimum-scale=1.0" name="viewport">

		<title>FieldMon</title>
		<link rel="stylesheet" href="/bower/uikit/css/uikit.almost-flat.min.css">
		<script src="/bower/jquery/dist/jquery.min.js"></script>
		<script src="/bower/uikit/js/uikit.min.js"></script>

		<style>
		#content{
			margin: auto;
			padding: 20px;
			max-width: 1000px;
		}
		</style>

	</head>
	<body>
		<div class='uk-navbar'>

			<div class='uk-navbar-content uk-navbar-center uk-navbar-brand'>FieldMon</div>
		</div>



		<div id="content">
            <button id='connect-btn' class="uk-button uk-button-primary">Connect</button>&nbsp;&nbsp;&nbsp;&nbsp;
            <button id='disconnect-btn' class="uk-button">Disconnect</button><br>
			<button id='move-btn' class="uk-button">Move</button><br>
            <br>
            Status: <div id="status"></div>
        </div>

        <script>
            $("#connect-btn").on("click", function(){
                $.ajax({
					url: "/drone/connect",
					success: function(response){
						$("#status").html(response);
					}
				});
            });

            $("#disconnect-btn").on("click", function(){
                $.ajax({
					url: "/drone/disconnect",
					success: function(response){
						$("#status").html(response);
					}
				});
            });

			$("#move-btn").on("click", function(){
                $.ajax({
					url: "/drone/move",
					success: function(response){
						$("#status").html(response);
					}
				});
            });
        </script>
	</body>
</html>
