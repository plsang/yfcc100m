<?php

require_once "nsc-web-AppConfig.php";
require_once "nsc-TRECVIDTools.php";
set_time_limit ( 360 );

$nPlayerWidth = 400;
$nPlayerHeight = $nPlayerWidth*3/4;

if(isset($_REQUEST['localDir']))
{
	$szLocalDir = $_REQUEST['localDir'];
}
else
{
	$szLocalDir = "."; 
}

if(isset($_REQUEST['videoID']))
{
	$szVideoID = $_REQUEST['videoID'];
}
else
{
	$szVideoID = ""; 
}

if(isset($_REQUEST['vFormat']))
{
	$szVideoFmt = $_REQUEST['vFormat'];
}
else
{
	$szVideoFmt = ""; 
}


if(isset($_REQUEST['oldvideoPath']))
{
	$szOldVideoPath = $_REQUEST['oldvideoPath'];
}
else
{
	$szOldVideoPath = ""; 
}


if(isset($_REQUEST['videoPath']))
{
	$szVideoPath = $_REQUEST['videoPath'];
}
else
{
	$szVideoPath = ""; 
}

$szLocalVideoURL = sprintf("%s/%s", $szLocalDir, $szVideoPath);

if(isset($_REQUEST['shotStart']))
{
	$nShotStart = $_REQUEST['shotStart'];
}
else
{
	$nShotStart = 0;
}

if(isset($_REQUEST['shotDuration']))
{
	$nShotDuration = $_REQUEST['shotDuration'];
}
else
{
	$nShotDuration = 0;
}

if(isset($_REQUEST['autoStart']))
{
	$nAutoStart = $_REQUEST['autoStart'];
}
else
{
	$nAutoStart = "true";
}

if(isset($_REQUEST['frameRate']))
{
	$nFrameRate = $_REQUEST['frameRate'];
}
else
{
	$nFrameRate = 30;
}

$szTmpDir = '/net/per610a/export/das11f/plsang/codes/yfcc100m/view/tmp';

//$nPos = intval($nShotStart/$nFrameRate);
//printf("<P>Period: [%d-%d]<BR>\n", $nPos, $nPos+$nShotDuration/$nFrameRate);

printf('<head>');
printf('<link href="./video-js/video-js.css" rel="stylesheet">');
printf('<script src="./video-js/video.js"></script>');
printf('</head>');

printf('<body>');
$szNewVideoPath = sprintf('./webm/%s.webm', $szVideoID);
$szPageParams = sprintf("videoID=%s&videoPath=%s&oldvideoPath=%s&vFormat=%s", $szVideoID, $szNewVideoPath, $szVideoPath, 'webm');
$szNewUrl = sprintf('%s?%s', $_SERVER['PHP_SELF'], $szPageParams);

printf('<video id="my_video_1" class="video-js vjs-default-skin" controls');
printf(' preload="auto" width="640" height="480" poster="my_video_poster.png"');
printf(' data-setup="{}">');
if($szVideoFmt == 'webm'){
    // check if video exist
    if(!file_exists($szNewVideoPath)){
        $arCmdLine[] = sprintf('source /net/per610a/export/das11f/plsang/codes/yfcc100m/view/bash.sh');
        
        $szRootWebDir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/view';
        
        $szCmdLine = sprintf('/net/per610a/export/das11f/plsang/usr/bin/ffmpeg -i %s/%s -vcodec libvpx -cpu-used 4 -threads 8 %s/%s', $szRootWebDir, $szOldVideoPath, $szRootWebDir, $szNewVideoPath);

        $arCmdLine[] = $szCmdLine;

        //$szFPCmdFN = sprintf('%s.sh', tempnam( $szTmpDir, 'vid' ));
        $szFPCmdFN = tempnam( $szTmpDir, 'webm' );
        saveDataFromMem2File($arCmdLine, $szFPCmdFN);

        $szCmdLine = sprintf("chmod 777 %s", $szFPCmdFN);
        system($szCmdLine);
        system($szFPCmdFN);
        deleteFile($szFPCmdFN);
    }
    
    printf(' <source src="'.$szVideoPath.'" type="video/webm">');    
}else{
    printf(' <source src="'.$szVideoPath.'" type="video/mp4">');
}
printf('</video>');

if($szVideoFmt != 'webm'){ 
    printf('Click <a href="%s">here</a> if the video is not playing!', $szNewUrl);
}

$arCmdLine[] = sprintf('cd %s', $szTmpDir);
$arCmdLine[] = sprintf('source /net/per610a/export/das11f/plsang/codes/yfcc100m/view/bash.sh');

$szCmdLine = sprintf('/net/per900a/raid0/plsang/usr.local/bin/python /net/per610a/export/das11f/plsang/codes/yfcc100m/yfcc100m_read_table.py --id %s', $szVideoID);

$arCmdLine[] = $szCmdLine;

//$szFPCmdFN = sprintf('%s.sh', tempnam( $szTmpDir, 'vid' ));
$szFPCmdFN = tempnam( $szTmpDir, 'vid' );
saveDataFromMem2File($arCmdLine, $szFPCmdFN);

$szCmdLine = sprintf("chmod +x %s", $szFPCmdFN);
system($szCmdLine);
exec($szFPCmdFN, $info, $retval);
if($retval == 0) {
    
    printf("<P><b>Title</b>: %s <BR>\n", $info[0]);
    printf("<P><b>Description</b>: %s <BR>\n", $info[1]);
    printf("<P><b>User tags</b>: %s <BR>\n", $info[2]);
    printf("<P><b>Machine tags</b>: %s <BR>\n", $info[3]);
}

deleteFile($szFPCmdFN);

printf('</body>');

?>
