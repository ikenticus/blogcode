<?php
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://myexternalip.com/");
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
    $doc = curl_exec($ch);
?>
