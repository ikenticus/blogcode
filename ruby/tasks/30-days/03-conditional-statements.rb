#!/bin/ruby

require 'json'
require 'stringio'



N = gets.to_i
if N % 2 == 1 or (N >= 6 and N <= 20)
    puts 'Weird'
else
    puts 'Not Weird'
end

