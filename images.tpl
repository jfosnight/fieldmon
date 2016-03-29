<!DOCTYPE html>
<html>
	<head>

		<title>Images - FieldMon</title>
		<link rel="stylesheet" href="/bower/uikit/css/uikit.almost-flat.min.css">
		<script src="/bower/jquery/dist/jquery.min.js"></script>
		<script src="/bower/uikit/js/uikit.min.js"></script>

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
			
			<div class='uk-navbar-content uk-navbar-center uk-navbar-brand'>Images - FieldMon</div>
		</div>
		<div id="content">
			<h2>Images</h2>
			Take Picture <a href="/image/take">New Picture</a><br>
			<br>
			
			<table class='uk-table uk-table-striped uk-table-condensed'>
				<thead>
					<tr>
						<th>ID</th>
						<th>Filename</th>
						<th>Timestamp</th>
						<th>URL</th>
					</tr>
				</thead>
				% for image in images:
				<tr>
					<td>{{image[0]}}</td>
					<td>{{image[1]}}</td>
					<td>{{image[2]}}</td>
					<td><a href="/image/{{image[1]}}" target="_blank">Image {{str(image[0]).zfill(4)}}</a></td>
				</tr>
				% end
			</table>
		</div>
	</body>
</html>


