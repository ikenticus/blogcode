Issue 410: Spellchecker
===
A client has asked us to write a custom API to help them determine if a word is spelled according to their corporate standards. If not, the API should return some suggestions.

The client has specified that word does not conform if it:
- It has repeating characters (i.e. balllooooon)
- It is missing one or more vowels (i.e. balln)
- It has mixed-casing (i.e. BAllOOn)
    - Note: “Hello” and “HELLO” are correct and should not be considered mixed-casing.
- It has a combination of a, b and c type errors (i.e. bllllLLlln)

They have provided a dictionary of acceptable words in `dictionary.txt` contained in this archive.

They client has already developed against a similar API built by another client, so the endpoint must:
- Be `/spellcheck/{word}`
- Run on port `31337`.
- Return `404` if the word is not found
- Return `200` if the word is found
    - The body of the response should include acceptable spelling suggestions if the word is misspelled.

They've provided us some examples of what their other implementation returns:
```
URL: http://localhost:31337/spell/car

Response Code: 200
Response Body:
{"suggestions": [], "correct": true}
```
```
URL: http://localhost:31337/spell/caR

Response Code: 200
Response Body:
{"suggestions": ["car", "care"], "correct": false}
```

Keep in mind that this code will need to be maintained for a very long time, and may be subject to random changes and feature requests from the client which must be implemented by other developers. Remember that we host all of our infrastructure on Debian-based containers.

Since we're so cool and using microservices, your choice of language isn't important, but keep in mind the above points.

Our lawyers haven't signed off on any Open Source libraries that do spellchecking, so please don't use any. They've given us the green light for all other types of libaries (weird, right?)

When finished, send it back our way.