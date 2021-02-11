# https://norvig.com/spell-correct.html

import re
import sys

from flask import Flask, request, jsonify
from collections import Counter

app = Flask(__name__)
ALPHA = 'abcdefghijklmnopqrstuvwxyz'

def words(text):
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('dictionary.txt').read()))

def suggestions(word):
    'Word suggestions from the dictionary'
    return list(known([word]) or known(mod1(word)) or known(mod2(word)) or [word])

def known(words):
    'Retrieve all known words from the dictionary'
    return set(w for w in words if w in WORDS)

def omit(sets):
    'Word variations with one character omitted'
    return [w + e[1:] for w, e in sets if e]

def swap(sets):
    'Word variations with one character pair swapped'
    return [w + e[1] + e[0] + e[2:] for w, e in sets if len(e)>1]

def sub(sets):
    'Word variations with one alphabet character substituted'
    return [w + c + e[1:] for w, e in sets if e for c in ALPHA]

def add(sets):
    'Word variations with one alphabet character added'
    return [w + c + e for w, e in sets for c in ALPHA]

def mod1(word):
    'Single modification from word'
    sets = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    return set(omit(sets) + swap(sets) + sub(sets) + add(sets))

def mod2(word):
    'Double modification from word'
    return (m2 for m1 in mod1(word) for m2 in mod1(m1))

def repeat(word):
    'Returns True if more than 2 repeating characters in a row'
    groups = []
    for c in word:
        if groups and groups[-1][-1] == c:
            groups[-1] += c
        else:
            groups.append(c)
    return True if max([len(g) for g in groups]) > 2 else False

def mixed(word):
    '''
        Returns True if word has mixed casing: (i.e. BAllOOn)
        Note: “Hello” and “HELLO” are correct and not considered mixed-casing.
    '''
    sets = len(re.split('[A-Z]', word[1:]))
    return True if sets > 1 and word != word.upper() else False

def suffix(word):
    'Removed commonly repeated suffices from word'
    suffices = ['less', 'ly', 'ness']
    shorten = False
    for s in suffices:
        if word.endswith(s):
            word = word[:-len(s)]
            shorten = True
    if shorten:
        word = suffix(word)
    return word

def triple(sets):
    'Remove common triple consonents from set'
    good = ['ght', 'nch', 'nth', 'rch', 'rth', 'tch' ]
    clean = []
    for s in sets:
        for g in good:
            if s.startswith(g):
                s = s[len(g):]
        if len(s) == 3 and s[0] == s[1]:
            s = s[2:]
        clean.append(s)
    return clean

def missing(word):
    '''
        Return True if word is missing one or more vowels (i.e. balln)
        Note: This is trickier to detect so we will use the following assumptions:
            - no consonants will have clusters of more than two
            - exceptions to this seem to be 'ght', 'nch', 'rch', 'tch'
                (weight, ranch, birch, patch, birthright), perhaps more added later
            - usually a consonent following a repeated consonent is valid (ballpark)
            - certain suffices are valid, like -less, -ly, ness (selflessnessly)
    '''
    word = suffix(word)
    sets = triple(re.split('[aeiouAEIOU]', word))
    return True if max([len(s) for s in sets]) > 2 else False

def invalid(word):
    'Validate the specified word against the corporate standards'
    return repeat(word) or missing(word) or mixed(word)

@app.route("/spellcheck/<string:word>", methods=["GET"])
def spellcheck(word):
    '''
    Check if word conforms to corporate standards
    Responses:
        200: word is valid
        404: word is invalid
    NOTE: Based on the criteria of the example, it is assumed that
        if word passes validity checks it will not be checked against
        the dictionary, which was provided for suggestion-purposes only
    '''
    if invalid(word):
        return {'suggestions': suggestions(word.lower()), 'correct': False}, 404
    return {'suggestions': [], 'correct': True}, 200

if __name__ == '__main__':
    # print(missing(sys.argv[1]))
    app.run(debug=True, host='0.0.0.0', port=31337)
