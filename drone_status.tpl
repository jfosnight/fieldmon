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
            <br>
            Status: <div id="status"></div>
        </div>

        <script>
            var ws = null;

            $("#connect-btn").on("click", function(){
                ws = new WebSocket("ws://localhost/ws/drone/status");
                ws.onopen = function() {
                    $("#status").html("Connected");
                };
                ws.onmessage = function (evt) {
                    $("#status").html(evt.data);
                };
            });

            $("#disconnect-btn").on("click", function(){
                ws.close()
            });
        </script>
	</body>
</html>
