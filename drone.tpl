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
			<ul class='uk-navbar-nav'>
				<li><a href="/"><i class='uk-icon-home'></i> Home</a></li>
			</ul>

			<div class='uk-navbar-content uk-navbar-center uk-navbar-brand'>FieldMon</div>
		</div>



		<div id="content">
            <button id='connect-btn' class="uk-button uk-button-primary">Connect</button>&nbsp;&nbsp;&nbsp;&nbsp;
            <button id='disconnect-btn' class="uk-button">Disconnect</button>&nbsp;&nbsp;&nbsp;&nbsp;

			Drone Connection Status: <span id="connection-status" class="uk-text-large"></span>
			<br>
			<hr>
			<button id='takeoff-btn' class="uk-button">Take Off</button>&nbsp;&nbsp;&nbsp;&nbsp;
			<!-- <button id='move-btn' class="uk-button">Move</button>&nbsp;&nbsp;&nbsp;&nbsp; -->
			<button id='mission-btn' class="uk-button uk-button-primary">Fly Mission</button>&nbsp;&nbsp;&nbsp;&nbsp;
			<button id='rtl-btn' class="uk-button">Return Home</button><br>
			<br>
			Status: <span id="status" class="uk-text-large"></span>
			<br>
			<hr>
			<h2>Real-time Drone Info</h2>

			<!--<button id='ws-connect-btn' class="uk-button uk-button-primary">Connect</button>&nbsp;&nbsp;&nbsp;&nbsp;
            <button id='ws-disconnect-btn' class="uk-button">Disconnect</button><br>
			<br>-->
			<!--<h3>Drone Stats</h3>-->
			<div id="ws-status"></div>
        </div>

        <script>
            $("#connect-btn").on("click", function(){
				$("#connection-status").html("<div class='uk-badge uk-badge-warning uk-text-large'>Connecting...</div>");
                $.ajax({
					url: "/drone/connect",
					success: function(response){
						var html = "";
						if(response === "Connected to Drone" || response === "Already Connected"){
							wsConnect();
							html += "<div class='uk-badge uk-badge-success uk-text-large'>Connected</div>";
						} else {
							html += "<div class='uk-badge uk-badge-danger uk-text-large'>" + response + "</div>";
						}
						$("#connection-status").html(html);
					}
				});
            });

            $("#disconnect-btn").on("click", function(){
                $.ajax({
					url: "/drone/disconnect",
					success: function(response){
						var html = "";
						wsDisconnect();
						if(response === "Disconnected"){
							html += "<div class='uk-badge uk-badge-danger uk-text-large'>Disconnected</div>";
						} else {
							html += "<div class='uk-badge uk-badge-danger uk-text-large'>" + response + "</div>";
						}
						$("#connection-status").html(html);
					}
				});
            });

			$("#takeoff-btn").on("click", function(){
				$("#status").html("Sending Command");
                $.ajax({
					url: "/drone/takeoff",
					success: function(response){
						$("#status").html(response);
					}
				});
            });

			$("#move-btn").on("click", function(){
				$("#status").html("Sending Command");
                $.ajax({
					url: "/drone/move",
					success: function(response){
						$("#status").html(response);
					}
				});
            });

			$("#mission-btn").on("click", function(){
				$("#status").html("Sending Command");
                $.ajax({
					url: "/drone/mission",
					success: function(response){
						$("#status").html(response);
					}
				});
            });

			$("#rtl-btn").on("click", function(){
				$("#status").html("Sending Command");
                $.ajax({
					url: "/drone/rtl",
					success: function(response){
						$("#status").html(response);
					}
				});
            });


			var ws = null;
			function wsConnect(){
				if(!ws){
					ws = new WebSocket("ws://" + window.location.host + "/ws/drone/status");
	                ws.onopen = function() {
	                    $("#ws-status").html("Connected");
	                };
	                ws.onmessage = function (evt) {
	                    $("#ws-status").html(evt.data);
	                };
					ws.onclose = function(){
						$("#ws-status").html("Disconnected");
						var html = "<div class='uk-badge uk-badge-danger uk-text-large'>Disconnected</div>";
						$("#connection-status").html(html);
					}
				}
			}

			function wsDisconnect(){
				if(ws){
					ws.close();
					ws = null;
				}
				console.log("WS: ", ws);
			}


            $("#ws-connect-btn").on("click", function(){
				wsConnect();
            });

            $("#ws-disconnect-btn").on("click", function(){
				wsDisconnect();
            });
        </script>
	</body>
</html>
