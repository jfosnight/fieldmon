<!DOCTYPE html>
<html>
	<head>
		<meta content="width=device-width,minimum-scale=1.0" name="viewport">

		<title>New Node - FieldMon</title>
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

		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
	    <script type="text/javascript">
	      google.charts.load('current', {'packages':['corechart']});
	      google.charts.setOnLoadCallback(drawChart);

	      function drawChart() {
	        var data = google.visualization.arrayToDataTable([
	          ['Timestamp', 'Temperature', 'Humidity']
			  % for data in sensor_data:
			  	,[{{data['timestamp']}},{{data['temperature']}},{{data['humidity']}}]
			  % end
	        ]);

	        var options = {
	          title: 'Test Chart',
	          curveType: 'function',
	          legend: { position: 'bottom' }
	        };


		% if sensor_data:
	        	var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
	        	chart.draw(data, options);
		% else:
			document.getElementById("curve_chart").innerHTML = "<b>No Data Uploaded Yet</b>"
		% end

	      }
	    </script>

	</head>
	<body>
		<div class='uk-navbar'>
			<ul class='uk-navbar-nav'>
				<li><a href="/"><i class='uk-icon-home'></i> Home</a></li>
                <li><a href="/node/"><i class='uk-icon-arrow-left'></i> Back</a></li>
			</ul>
		</div>
		<div id="content">
			<h2>Sensor Node</h2>
			<br>
			<div class="uk-grid">
				<div class="uk-width-1-3">
					<b>Name</b><br>
		            {{node['name']}}<br>
		            <br>
		            <b>Latitude</b><br>
		            {{node['lat']}}<br>
		            <br>
		            <b>Longitude</b><br>
		            {{node['lng']}}<br>

				    <br>
				    <a class="uk-button uk-button-primary" href="/node/{{node['id']}}/data">Upload Data</a>

		            <br>
					<br>
					<br>
					<a class="uk-button uk-button-danger uk-button-small" href="/node/{{node['id']}}/data/delete">Clear Data</a>
					&nbsp;&nbsp;
					<a class="uk-button uk-button-danger uk-button-small" href="/node/{{node['id']}}/delete">Delete Node</a>
					<br>


		            <br>
		            <h4><a data-uk-toggle="{target: '#edit-form'}"><i class='uk-icon-edit'></i> Edit</a></h4>
		            <form class='uk-form uk-hidden uk-form-horizontal' method='POST' id='edit-form'>
		                <div class='uk-form-row'>
		                    <label class='uk-form-label'>Name</label>
		                    <div class='uk-form-controls'>
		                        <input type='text' name='name' value='{{node['name']}}'>
		                    </div>
		                </div>
		                <div class='uk-form-row'>
		                    <label class='uk-form-label'>Latitude</label>
		                    <div class='uk-form-controls'>
		                        <input type='text' name='lat' value='{{node['lat']}}'>
		                    </div>
		                </div>
		                <div class='uk-form-row'>
		                    <label class='uk-form-label'>Longitude</label>
		                    <div class='uk-form-controls'>
		                        <input type='text' name='lng' value='{{node['lng']}}'>
		                    </div>
		                </div>
		                <br>
		                <div class='uk-form-row'>
		                    <label class='uk-form-label'></label>
		                    <div class='uk-form-controls'>
		                        <button type='submit' class='uk-button uk-button-primary'><i class='uk-icon-save'></i> Update Node</button>
		                    </div>
		                </div>
		            </form>
				</div>

				<!-- Column 2-->
				<div class="uk-width-2-3">
					<h3>Sensor Data</h3>

					<div id="curve_chart" style="width: 100%; height: 400px"></div>

					<table class='uk-table uk-table-striped uk-table-condensed'>
						<thead>
							<tr>
							</tr>
						</thead>
						% for data in sensor_data:
						<tr>
							% for val in data:
								<td>{{val}}</td>
							% end
						</tr>
						% end
					</table>
				</div>

			<!-- End Grid -->
			</div>

		<!-- End Content -->
		</div>
	</body>
</html>
