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
			
			<div class='uk-navbar-content uk-navbar-center uk-navbar-brand'>Images - FieldMon</div>
		</div>
		<div id="content">
			<h2>Images</h2>
			<!--Take Picture <a href="/image/take">New Picture</a><br>-->
			<button class='uk-button uk-button-primary new-image-btn'><i class='uk-icon-image'></i> Take Picture</button><br>
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
				
				% from datetime import datetime, tzinfo, timedelta
				% td = timedelta(hours=5)
				<tr>
					<td>{{image[0]}}</td>
					<td>{{image[1]}}</td>
					<td>{{(datetime.strptime(image[2], "%Y-%m-%d %H:%M:%S")-td).ctime()}}</td>
					<td><a href="/image/{{image[1]}}" target="_blank">Image {{str(image[0]).zfill(4)}}</a></td>
				</tr>
				% end
			</table>
		</div>
		<script>
			$(".new-image-btn").on('click', function(event){
				var mssg = $.UIkit.notify({message: "Taking Picture"});
				$.ajax({
					url: "/image/take",
					method: "GET",
					dataType: "json",
					success: function(response){
						if(response.status === 'error'){
							mssg.close();
							$.UIkit.notify({message: "Error Taking Picture", status: "danger"});
							console.log(response);
						} else {
							var html = "";
							
							html += "<tr>";
							
							html += "<td>";
							html += response.body.id;
							html += "</td>";
							
							html += "<td>";
							html += response.body.file_name;
							html += "</td>";
							
							html += "<td>";
							html += response.body.timestamp;
							html += "</td>";
							
							html += "<td>";
							html += "<a href='/image/" + response.body.file_name + "' target='_blank'>Image " + response.body.id + "</a>";
							html += "</td>";
							
							html += "</tr>";
							$("table").append(html);
							
							mssg.close();
							$.UIkit.notify({message: "Picture Taken", status: "success"});
						}
					},
					error: function(error){
						console.log(error);
					}
				});
			});
		</script>
	</body>
</html>


