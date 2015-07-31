<?php
    $str = "('9889433636', 9)";
    //$pattern = "/\(\'?P<id>(\d+)\', ?P<part>\d+\)/";
    $pattern = "/(?P<id>\d+)', (?P<part>\d?)/";
    preg_match($pattern, $str, $matches);
    print_r($matches);
    exit();
    
    require_once "nsc-web-AppConfig.php";
    require_once "nsc-TRECVIDTools.php";

    $szTmpDir = '/net/per610a/export/das11f/plsang/codes/yfcc100m/view/tmp';
	$arCmdLine[] = sprintf('cd %s', $szTmpDir);
	$arCmdLine[] = sprintf('source /net/per610a/export/das11f/plsang/coco2014/selective_search/bash.sh');
    
	$szCmdLine = sprintf('/net/per900a/raid0/plsang/usr.local/bin/python /net/per610a/export/das11f/plsang/codes/yfcc100m/view/test.py');

	$arCmdLine[] = $szCmdLine;

	$szFPCmdFN = sprintf('%s/%s.sh', $szTmpDir, 'tmp');
	saveDataFromMem2File($arCmdLine, $szFPCmdFN);

	$szCmdLine = sprintf("chmod +x %s", $szFPCmdFN);
	system($szCmdLine);
    //exec('/net/per900a/raid0/plsang/usr.local/bin/python /net/per610a/export/das11f/plsang/codes/yfcc100m/view/test.py', $output, $retval);
    //system($szFPCmdFN, $retval);
    exec($szFPCmdFN, $output, $retval);
    echo $retval;
    print_r($output);