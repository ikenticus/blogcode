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
         \
      X A L - is_word = false
       /    \
      D      L - is_word = true
              \
               O - is_word = true

'''

# use a class instead of hash/dict

class Node:
    def __init__(self, letter):
        self.data = letter
        self.next = {}
        self.word = False

class Tree:
    def insert(self, root, word):
        if root == None:
            root = Node('')

        if len(word) > 0:
            letter = word[0]
            if letter not in root.next.keys():
                root.next[letter] = Node(letter)
            if len(word) > 1:
                self.insert(root.next[letter], word[1:])
            else:
                root.next[letter].word = True
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
    for letter in p:
        if letter in root.next.keys():
            root = root.next[letter]
    print recurse(p, root, [])

def recurse(word, root, out=[]):
    if root.word:
        out.append(word)
    for k in root.next.keys():
        recurse(word + k, root.next[k], out)
    return out

root = build_tree()
suggest('h', root)
suggest('pi', root)
suggest('hel', root)
suggest('pie', root)
