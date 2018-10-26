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

'''

# quick and dirty would be to loop through the list

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

def suggest(p):
    out = []
    for w in words:
        if w.startswith(p) and len(w) > len(p):
            out.append(w)
    print out

suggest('h')
suggest('pi')
suggest('hel')
suggest('pie')
