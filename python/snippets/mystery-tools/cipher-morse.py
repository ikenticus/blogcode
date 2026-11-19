import os
import sys
from pprint import pprint

#
# Dash: 3 units long (three times a dot).
# Within a letter: 1 unit of silence between dots and dashes.
# Between letters: 3 units of silence.
# Between words: 7 units of silence (often written with a / in plain text
#
# Developed in the 1830s and 1840s by Samuel Morse, Alfred Vail, and Joseph Henry for electrical telegraphy,
# the original American Morse code was largely replaced by International Morse code (introduced in 1851)
#

dit = '.'   # original dot
dah = '-'   # original dash
sep = ' '   # original sep

gap = os.getenv('GAP', sep)                 # gap between symbols
dot = os.getenv('DOT', dit)
dash = os.getenv('DASH', dah)
char = os.getenv('CHAR', gap * 3)           # sep between letters/characters
word = os.getenv('WORD', gap + '/' + gap)   # sep between words

code = {
    'A': '. -',
    'B': '- . . .',
    'C': '- . - .',
    'D': '- . .',
    'E': '.',
    'F': '. . - .',
    'G': '- - .',
    'H': '. . . .',
    'I': '. .',
    'J': '. - - -',
    'K': '- . -',
    'L': '. - . .',
    'M': '- -',
    'N': '- .',
    'O': '- - -',
    'P': '. - - .',
    'Q': '- - . -',
    'R': '. - .',
    'S': '. . .',
    'T': '-',
    'U': '. . -',
    'V': '. . . -',
    'W': '. - -',
    'X': '- . . -',
    'Y': '- . - -',
    'Z': '- - . .',

    '0': '- - - - -',
    '1': '. - - - -',
    '2': '. . - - -',
    '3': '. . . - -',
    '4': '. . . . -',
    '5': '. . . . .',
    '6': '- . . . .',
    '7': '- - . . .',
    '8': '- - - . .',
    '9': '- - - - .',

    '!': '- . - . - -',
    '@': '. - - . - .',
    '$': '. . . _ . . _',
    '&': '. - . . .',
    '(': '- . - - .',
    ')': '- . - - . -',
    '-': '- . . . . -',
    '_': '. . - - . -',
    '=': '- . . . -',
    '+': '. - . - . -',

    ':': '- - - . . .',
    ';': '- . - . - .',
    "'": '. - - - - .',
    '"': '. - . . - .',
    ',': '- - . . - -',
    '.': '. - . - . -',
    '/': '- . . - .',
    '?': '. . - - . .',
}
flip = dict(map(reversed, code.items()))
#print(flip)

input = sep.join(sys.argv[1:]).upper()
#print(input)

decode = os.getenv('DECODE')
output = ''
if not decode:
    for i in input:
        if i == sep:
            output = output.rstrip(char) + word
            #output += word
        elif i in code.keys():
            output += '%s%s' % (code[i].replace(dit,dot).replace(dah,dash).replace(sep,gap), char)
    output = output.rstrip(char)
else:
    for w in input.split(word):
        #print("decoding word: %s" % w)
        for c in w.split(char):
            #print("decoding char: %s" % c)
            if c in flip.keys():
                output += flip[c]
        output += sep
        
print(output)

