<!DOCTYPE html>
<html>
<head lang="en">
	<title>Downloads</title>
	<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
	<meta name="robots" content="noarchive" />
	<meta name="googlebot" content="noarchive" />
	<link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
	<div id="wrap">
	<h1>Downloads</h1>
<?php

	setlocale(LC_ALL, 'en_US.UTF8');

	foreach (glob("./incoming/*") as $path)
	{
		$docs[filectime($path)] = $path;
	}
	krsort($docs); // reverse sort by date (newest on top)
	print '<table>';
	foreach ($docs as $timestamp => $path)
	{
		print '<tr>';
		print '<td>' . date("d. M. Y: ", $timestamp) . '</td>';
		print '<td> <a href="download.php?file='. $path .'" >' . basename($path) .'</a></td><td align="right">'. filesize($path) .' bytes </td>';
		print '</tr>';
	}
	print '</table>';
?>
	</div>
</body>
</html>
