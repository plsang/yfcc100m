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

printf("<P><H1>View YLI MED Annotation </H1></P>\n");
printf("<FORM ACTION='nsc-web-View-YLIMED.php' TARGET='_blank'>\n");

printf("</SELECT>\n");

$even_list_file = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/yli-med/YLI-MED_v.1.2.0/events/events.txt';
loadListFile($arEvents, $even_list_file);

printf("<P><H3>Select event: <BR>\n");
printf("<SELECT NAME='vEvent'>\n");
for($i=0; $i<10; $i++)
{	
	$event = sprintf('Ev%d', 101+$i);
    $arParts = explode(" ", $arEvents[$i]);
    
	printf("<OPTION VALUE='%s %s %s'>%s - %s </OPTION>\n", $event, $arParts[1], $arParts[2], $event, $arParts[1] );
}

printf("</SELECT>\n");

printf("<P><H3>Select type: <BR>\n");
printf("<SELECT NAME='vType'>\n");

printf("<OPTION VALUE='Positive' SELECTED>Positive</OPTION>\n");
printf("<OPTION VALUE='Near_Miss'>Near_Miss</OPTION>\n");
printf("<OPTION VALUE='Related'>Related</OPTION>\n");

printf("</SELECT>\n");

printf("<P><INPUT TYPE='SUBMIT' value='Submit' name='vSubmit'>\n");
printf("</FORM>\n");

?>