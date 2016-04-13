<!DOCTYPE html>
<html>
	<head>
		<meta content="width=device-width,minimum-scale=1.0" name="viewport">

		<title>Upload Sensor Data - FieldMon</title>
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
                <li><a href="/node/"><i class='uk-icon-arrow-left'></i> Back</a></li>
			</ul>
		</div>
		<div id="content">
			<h2>Upload Sensor Data</h2>
			<br>
            <form class='uk-form uk-form-horizontal' method='POST' enctype="multipart/form-data">
                <div class='uk-form-row'>
                    <label class='uk-form-label'>Data File</label>
                    <div class='uk-form-controls'>
                        <input type='file' name='data'>
                    </div>
                </div>
                <br>
                <div class='uk-form-row'>
                    <label class='uk-form-label'></label>
                    <div class='uk-form-controls'>
                        <button type='submit' class='uk-button uk-button-primary'><i class='uk-icon-upload'></i> Upload Data</button>
                    </div>
                </div>
            </form>
		</div>
	</body>
</html>
