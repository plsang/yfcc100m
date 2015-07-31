<?php

/**
 * 		View concept annotation form - Web app.
 *
 * 		Copyright (C) 2010 Duy-Dinh Le
 * 		All rights reserved.
 * 		Email		: ledduy@gmail.com, ledduy@ieee.org.
 * 		Version		: 1.0.
 * 		Last update	: 13 Jan 2010.
 */

require_once "nsc-web-AppConfig.php";
require_once "nsc-TRECVIDTools.php";

// show form
$szRootProjectDir = $gszRootProjectDir;
$szVideoArchiveName = $gszVideoArchiveName;
$szFPConceptListMapFN = './data/metadata/parts.txt';

loadListFile($arConceptNameList, $szFPConceptListMapFN);
$nParts = sizeof($arConceptNameList);

printf("<P><H1>View Extracted keyframes </H1></P>\n");
printf("<FORM ACTION='nsc-web-ViewVideo.php' TARGET='_blank'>\n");

printf("</SELECT>\n");

printf("<P><H3>Select part: <BR>\n");
printf("<SELECT NAME='vPartName'>\n");

for($i=0; $i<$nParts; $i++)
{
	$szConceptName = $arConceptNameList[$i];
	
	$splits = explode(' >.< ', $szConceptName);
	
	printf("<OPTION VALUE='%s'>%s</OPTION>\n", $szConceptName, $szConceptName);
}
printf("</SELECT>\n");

printf("<P><INPUT TYPE='SUBMIT' value='Submit' name='vSubmit'>\n");
printf("</FORM>\n");

?>