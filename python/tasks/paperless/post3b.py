'''

Given an input of dictionary words:

```
[
  "headquarters",
  "helium",
  "hello",
  "help",
  "hex",
  "hexagon",
  "picasso",
  "picture",
  "pie",
  "pool"
]
```

Please write a function that will take in a prefix and return an array of suggested words.

Examples:

```
suggest('h')   // ["headquarters", "helium", "hello", "help", "hex", "hexagon"]
suggest('pi')  // ["picasso", "picture", "pie"]
suggest('hel') // ["helium", "hello", "help"]
suggest('pie') // []
```

If the dictionary is complete and very large, looping through all and checking startswith
is not operationally efficient, try to build a letter node tree:

      H
       \
        E
       /|\  (potentially 26 children)
      X A L - is_word = false
       /   \
      D     L - is_word = true
             \ 
              O - is_word = true

'''
    
# of course I initially tried to build a dict

import json 

z = 'is_word'

tree = {} 
def build_tree():
    words = [
      "headquarters",
      "helium",
      "hello",
      "help",
      "hex",
      "hexagon",
      "picasso",
      "picture",
      "pie",
      "pool"
    ]
    
    for word in words:
        t = tree
        for c in word:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[z] = True

def suggest(p):
    t = tree
    for c in p:
       if c in t:
            t = t[c] 
    #print json.dumps(t, sort_keys=True, indent=2)
    print '%s:' % p,
    print recurse(p, t, [])
    
def recurse(p, t, out=[]):
    if z in t:
        out.append(p)
    for k in t.keys():
        if k != z:
            recurse(p + k, t[k], out)
    return out
        
build_tree()
#print json.dumps(tree, sort_keys=True, indent=2)

suggest('h')
suggest('pi')
suggest('hel')
suggest('pie')

