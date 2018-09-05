<?php

// Complete the solve function below.
function solve($meal_cost, $tip_percent, $tax_percent) {
    $tip = $tip_percent / 100;
    $tax = $tax_percent / 100;
    printf("The total meal cost is %.0f dollars.\n", $meal_cost * (1 + $tip + $tax));
}

$stdin = fopen("php://stdin", "r");

fscanf($stdin, "%lf\n", $meal_cost);

fscanf($stdin, "%d\n", $tip_percent);

fscanf($stdin, "%d\n", $tax_percent);

solve($meal_cost, $tip_percent, $tax_percent);

fclose($stdin);

