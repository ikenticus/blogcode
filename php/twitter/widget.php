<?php

/* 
    Twitter Widget Proxy/Cache Script
    Written April 2012 by ikenticus
*/

$interval = 30; // minimum number of seconds between API calls
$restrict = "ONLY_ALLOW_REQUESTS_TO_THIS_TWITTER_PROFILE";

$debug = 0;
$unauth = 0;
$profile = '';
$list_id = '';
$params = array();
foreach ($_GET as $k => $v) {
    switch ($k) {
        case 'debug':
            $debug = $v;
            break;
        case 'wtype':
            $wtype = $v;
            break;
        case 'profile':
            $profile = $v;
            break;
        case 'list_id':
            $list_id = $v;
            break;
        default:
            $params[] = "$k=$v";
    }
}

if ($profile && $list_id) {
    if ($profile != $restrict) $unauth = 1;
    $url = "http://api.twitter.com/1/$profile/lists/$list_id/statuses.json?";
    $filename = "list_${profile}_$list_id.jsonp";
} elseif ($_GET['q']) {
    $search = $_GET['q'];
    if ($search != $restrict) $unauth = 1;
    $url = "http://search.twitter.com/search.json?";
    $filename = "search_$search.jsonp";
} else {
    $profile = $_GET['screen_name'];
    if ($profile != $restrict) $unauth = 1;
    switch ($wtype) {
        case 'faves':
            $url = "http://api.twitter.com/1/favorites.json?";
            $filename = "faves_$profile.jsonp";
            break;
        case 'profile':
            $url = "http://api.twitter.com/1/statuses/user_timeline.json?";
            $filename = "profile_$profile.jsonp";
            break;
    }
}

if ($unauth) {
    exit("You are using an unauthorized twitter account!\n");
}

$update = 1;
$epoch = time();
if (file_exists($filename)) {
    if (($epoch - filemtime($filename)) < $interval) $update = 0;
}
if ($update) {
    $url .= implode('&', $params);
    if ($debug) print "UPDATE: $url\n";
    $data = @file_get_contents($url);
    if ($data) {
        $file = fopen($filename, 'w+');
        if ($debug) print "WRITE: $filename\n";
        fwrite($file, $data);
    }
} else {
    $file = fopen($filename, 'r');
    if ($debug) print "READ: $filename\n";
    $data = fread($file);
}
fclose($file);
print $data;

?>
