import os
import sys
from pprint import pprint

sep = os.getenv('SEP', ' ')

def encode(num: int) -> str:
    val_map = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    roman_numeral = ""
    for value, symbol in val_map:
        count, num = divmod(num, value)
        roman_numeral += symbol * count
    return roman_numeral

def deroman(s: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    
    for char in reversed(s.upper()):
        curr_value = roman_map[char]
        if curr_value < prev_value:
            total -= curr_value
        else:
            total += curr_value
        prev_value = curr_value
        
    return total

input = sep.join(sys.argv[1:]).upper()
#print(input)

decode = os.getenv('DECODE')
output = ''
for i in input.split(sep):
    if not decode:
        output += '%s%s' % (encode(int(i)), sep)
    else:
        output += '%s%s' % (deroman(i), sep)
        
output = output.rstrip(sep)
print(output)

