<?php
$handle = fopen ("php://stdin","r");
$i = 4;
$d = 4.0;
$s = "HackerRank ";


// Declare second integer, double, and String variables.
$i2 = 1;
$d2 = 1.0;
$s2 = "";

// Read and save an integer, double, and String to your variables.
$i2 = fgets($handle);
$d2 = fgets($handle);
$s2 = fgets($handle);

// Print the sum of both integer variables on a new line.
print($i + $i2 . "\n");

// Print the sum of the double variables on a new line.
print(number_format($d + $d2, 1) . "\n");

// Concatenate and print the String variables on a new line
// The 's' variable above should be printed first.
print($s . $s2);


fclose($handle);
?>
