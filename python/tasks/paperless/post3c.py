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
is not operationally efficient, try to build a char node tree:

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

# use a class instead of hash/dict

import json

class Node:
    def __init__(self, char):
        self.data = char
        self.next = {}
        self.word = False
    def display(self, root, indent=2, tab=''):
        print '%s%s%s' % (tab, root.data, ' $' if root.word else '')
        tab += indent * ' '
        for k in root.next.keys():
            self.display(root.next[k], indent, tab)

class Tree:
    def insert(self, root, word):
        if root == None:
            root = Node('')
        if len(word) > 0:
            char = word[0]
            if char not in root.next.keys():
                root.next[char] = Node(char)
            if len(word) > 1:
                self.insert(root.next[char], word[1:])
            else:
                root.next[char].word = True
        return root


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

    tree = Tree()
    root = None
    for word in words:
        root = tree.insert(root, word)
    return root

def suggest(p, root):
    for char in p:
        if char in root.next.keys():
            root = root.next[char]
    print '%s:' % p,
    print recurse(p, root, [])

def recurse(word, root, out=[]):
    if root.word:
        out.append(word)
    for k in root.next.keys():
        recurse(word + k, root.next[k], out)
    return out

root = build_tree()
root.display(root, indent=1)

suggest('h', root)
suggest('pi', root)
suggest('hel', root)
suggest('pie', root)
