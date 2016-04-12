<!DOCTYPE html>
<html>
	<head>
		<meta content="width=device-width,minimum-scale=1.0" name="viewport">
	
		<title>Nodes - FieldMon</title>
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
            <a class='uk-button uk-button-primary' href='/node/new'>
                <i class='uk-icon-plus'></i>
                New Node
            </a>
			
			<table class='uk-table uk-table-striped uk-table-condensed'>
				<thead>
					<tr>
                        <th></th>
						<th>ID</th>
						<th>Name</th>
						<th>Lat</th>
                        <th>Lng</th>
                        <th>Timestamp</th>
					</tr>
				</thead>
				% for node in nodes:
				<tr>
                    <td><a class='uk-button uk-button-mini uk-button-primary' href='/node/{{node['id']}}'><i class='uk-icon-eye'></i> View</a></td>
					<td>{{node['id']}}</td>
					<td>{{node['name']}}</td>
					<td>{{node['lat']}}</td>
                    <td>{{node['lng']}}</td>
                    <td>{{node['timestamp']}}</td>
				</tr>
				% end
			</table>
		</div>
	</body>
</html>


