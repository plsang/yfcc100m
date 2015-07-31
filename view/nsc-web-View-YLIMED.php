<?php

printf('<head>');
printf('<link rel="stylesheet" href="./Magnific-Popup/dist/magnific-popup.css"> ');
printf('<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>');
printf('<script src="./Magnific-Popup/dist/jquery.magnific-popup.js"></script>');
printf('<script src="./popup.js"></script>');
printf('<link href="./video-js/video-js.css" rel="stylesheet">');
printf('<script src="./video-js/video.js"></script>');
printf('</head>');

/**
 * 		Do concept annotation - Web app.
 *
 * 		Copyright (C) 2010 Duy-Dinh Le
 * 		All rights reserved.
 * 		Email		: ledduy@gmail.com, ledduy@ieee.org.
 * 		Version		: 1.0.
 * 		Last update	: 13 Jan 2010.
 */

require_once "nsc-web-AppConfig.php";
require_once "nsc-TRECVIDTools.php";

/*
$szRootProjectDir = "/net/per900b/raid0/ledduy/nii-secode2";
$szRootVideoArchiveDir = "/net/per900b/raid0/ledduy/video.archive";
$szVideoArchiveName = "trecvid";
$szRootKeyFrameDir = sprintf("../../../../video.archive/keyframe/%s", $szVideoArchiveName);
$szRootAnnDir = sprintf("%s/metadata/annotation/%s", $szRootProjectDir, $szVideoArchiveName);
*/
$szRootProjectDir = $gszRootProjectDir;
$szRootVideoArchiveDir = $gszRootVideoArchiveDir;
$szVideoArchiveName = $gszVideoArchiveName;
$szRootVideoDir = './data';
$szRootAnnDir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/metadata/yli-med/YLI-MED_v.1.2.0/events';
$szRootKfDir = './data/thumbnail';


$szEventStr = $_REQUEST['vEvent'];
$szEventParts = explode(" ", $szEventStr);

$szEvent = $szEventParts[0];
$szEventName = $szEventParts[1];
$szMEDEvent = $szEventParts[2];

$szType = $_REQUEST['vType'];

if(isset($_REQUEST['vPage']))
    $nPageID = intval($_REQUEST['vPage']);
else $nPageID = 0;

//$szFilter = $_REQUEST['vFilter'];
//$szPat = $_REQUEST['vPat'];

$szBaseURL = sprintf("%s?vEvent=%s&vType=%s", $_SERVER['PHP_SELF'],
$szEventStr, $szType);

$szPageParam = sprintf("vEvent=%s&vType=%s", $szEventStr , $szType);

$szFPConceptVideosFN = sprintf('%s/%s/%s.%s.txt', $szRootAnnDir, $szEvent, $szEvent, $szType);

loadListFile($arConceptVideos, $szFPConceptVideosFN);

// loading look up table

//print_r($lookup);

$nNumVideos = sizeof($arConceptVideos);

printf("<P><H1> YLI MED Annotation </H1></P>");
printf("<P><H2> Event ID: %s - Event Name: %s - Video Type: %s - Total videos: %d </H2></P>\n", $szEvent, $szEventName, $szType, $nNumVideos);
printf("<P><H2> View TRECVID Definition of Event [%s] <A href='../trecvidmed14/view/eventtexts/%s.txt'>here </A> </H2></P>\n", $szEventName, $szMEDEvent);
$med_view_param = sprintf('%s >.< %s', $szMEDEvent, $szEventName);
$med_view_url = sprintf('../trecvidmed14/view/nsc-web-ViewEventKits-MED14.php?vEventName=%s&vEventSet=EK100&vEventType=positive&vMaxItemsPerPage=50&vSubmit=Submit', $med_view_param);
printf("<P><H2> View TRECVID Example Video of Event [%s] <A href='%s'>here </A> </H2></P>\n", $szEventName, $med_view_url);

#$nStartID = $nPageID*$nMaxImgsPerPage;
#$nEndID = min(($nPageID+1)*$nMaxImgsPerPage, $nNumKeyFrames);

$nNumPages = $nNumVideos;


//$nMaxItemsPerPage = max(50, $_REQUEST['vMaxItemsPerPage']);
$nMaxItemsPerPage = 20;

$nStartID = $nPageID*$nMaxItemsPerPage;
$nEndID = min(($nPageID+1)*$nMaxItemsPerPage, $nNumVideos);

$nNumPages = intval(($nNumVideos+$nMaxItemsPerPage-1)/$nMaxItemsPerPage);


printf("<P><H3>Page: ");
for($i=0; $i<$nNumPages; $i++)
{
    if($i!=$nPageID)
    {
        printf("<A HREF='%s?vPage=%s&%s'>%02d</A> ", $_SERVER['PHP_SELF'], $i, $szPageParam, $i+1);
    }
    else
    {
        printf("%02d ", $i+1);
    }
}
printf("</H3>\n");
//print_r($arData);

printf("<table border=\"5\" cellpadding=\"5\">");
printf("<tr>");
$nCols = 5;
$nCountItem = 0;

for ($ii=$nStartID; $ii<$nEndID; $ii++) 
{   
	$nCountItem++;
	printf("<td>");
	
    
    $arParts = explode(" ", $arConceptVideos[$ii]);
    
	$szVideoID = strval($arParts[0]);
    
    $szPartName = sprintf('yfcc100m_dataset-%d', $arParts[1]);
    
    $szVideoFile = sprintf("%s/%s/%s.mp4", $szRootVideoDir, $szPartName, $szVideoID); 
	
    $szThumbnailURL = sprintf("%s/%s/%s.jpg", $szRootKfDir, $szPartName, $szVideoID);
    if(!file_exists($szThumbnailURL))
    {
        $szThumbnailDir = dirname($szThumbnailURL);
        if(!file_exists($szThumbnailDir)){
            mkdir($szThumbnailDir);
        }
        
        $ffmpeg_cmd = "export LD_LIBRARY_PATH=/net/per610a/export/das11f/plsang/usr/lib && /net/per610a/export/das11f/plsang/usr/bin/ffmpeg -i $szVideoFile -deinterlace -an -ss 1 -t 00:00:01 -r 1 -y -vcodec mjpeg -f mjpeg $szThumbnailURL 2>&1";
        
        shell_exec($ffmpeg_cmd);
    }

    
    $szViewParam = sprintf("videoID=%s&videoPath=%s", $szVideoID, $szVideoFile);
	$szViewVideoURL = sprintf("nsc-web-VideoPlayer.php?%s", $szViewParam);
    
    /*
    printf('<div id="popup-%d" class="white-popup mfp-hide" style="position: relative;background: #FFF;padding: 20px;width: auto;max-width:640px;margin: 20px auto;">', $ii);
    printf('<video id="%s" class="video-js vjs-default-skin" controls', $szVideoID);
    //printf(' preload="auto" width="320" height="240" poster="%s"', $szThumbnailURL);
    printf(' preload="no" width="320" height="240" poster=""');
    printf(' data-setup="{}">');
    printf(' <source src="'.$szVideoFile.'" type="video/mp4">');
    printf('</video>');
    printf('</div>');
    */
    
    //printf('<a href="#popup-%d" class="open-popup-link">View video</a>', $ii);    
    printf("<B>%d. [%s]</A> <A HREF='%s' target='_blank'><IMG ALT='View' SRC='view-video-icon.png' BORDER='0' WIDTH='25' Title='Note: Tested on Chrome + HTML5'></A>\n", $ii+1, $szVideoID, $szViewVideoURL);
    
    //printf("<B>%d. [%s]</A> <A href='#popup-%d' class='open-popup-link'> <IMG ALT='View' SRC='view-video-icon.png' BORDER='0' WIDTH='25' Title='Note: Tested on Chrome + HTML5'></A>\n", $ii+1, $szVideoID, $ii);
	
	printf("<IMG ALT='%s' SRC='%s' BORDER='0'/>\n", $szVideoID, $szThumbnailURL);
        
	printf("</td>");
	
	if($nCountItem % $nCols == 0)
	{
        printf("</tr>");
		printf("<tr>");
	}
}

printf("</table>");

?>
