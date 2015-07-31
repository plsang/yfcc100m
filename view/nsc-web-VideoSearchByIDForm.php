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
$szFPConceptListMapFN = '/net/per610a/export/das11f/plsang/codes/yfcc100m/view/data/metadata/parts.txt';

loadListFile($arConceptNameList, $szFPConceptListMapFN);
$nParts = sizeof($arConceptNameList);

printf("<P><H1>Search by ID</H1></P>\n");

printf("<FORM ACTION='nsc-web-VideoSearchByID.php' TARGET='_blank'>\n");

printf("<P><H3>Video ID: <BR>\n");
printf("<P><INPUT TYPE='TEXT' name='vid'>\n");
printf("<P><INPUT TYPE='SUBMIT' value='Submit' name='vSubmit'>\n");
printf("</FORM>\n");

?>