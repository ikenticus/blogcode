#!/bin/ruby

require 'json'
require 'stringio'

# Complete the solve function below.
def solve(meal_cost, tip_percent, tax_percent)
    tip = tip_percent.to_f / 100
    tax = tax_percent.to_f / 100
    printf("The total meal cost is %.0f dollars.", meal_cost * (1 + tip + tax))
end

meal_cost = gets.to_f

tip_percent = gets.to_i

tax_percent = gets.to_i

solve meal_cost, tip_percent, tax_percent

