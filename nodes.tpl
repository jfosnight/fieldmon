<!DOCTYPE html>
<html>
	<head>
		<meta content="width=device-width,minimum-scale=1.0" name="viewport">
	
		<title>Images - FieldMon</title>
		<link rel="stylesheet" href="/bower/uikit/css/uikit.almost-flat.min.css">
		<script src="/bower/jquery/dist/jquery.min.js"></script>
		<script src="/bower/uikit/js/uikit.min.js"></script>
		
		<link rel="stylesheet" href="/bower/uikit/css/components/notify.almost-flat.min.css">
		<script src="/bower/uikit/js/components/notify.min.js"></script>

		<style>
		#content{
			margin: auto;
			padding: 20px;
			max-width: 1200px;
		}
		</style>

	</head>
	<body>	
		<div class='uk-navbar'>
			<ul class='uk-navbar-nav'>
				<li><a href="/"><i class='uk-icon-home'></i> Home</a></li>
			</ul>
		</div>
		<div id="content">
			<h2>Sensor Nodes</h2>
			<br>
			
			<table class='uk-table uk-table-striped uk-table-condensed'>
				<thead>
					<tr>
						<th>ID</th>
						<th>Name</th>
						<th>Lat</th>
						<th>Long</th>
						<th></th>
					</tr>
				</thead>
				% for node in nodes:
				<tr>
					<td>{{node[0]}}</td>
					<td>{{node[1]}}</td>
					<td>{{node[2]}}</td>
					<td>{{node[3]}}</td>
					<td><a href="/image/{{image[1]}}" target="_blank">Node {{node[3]}}</a></td>
				</tr>
				% end
			</table>
		</div>
	</body>
</html>


