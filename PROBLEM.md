# Implement a JSON parser

## Problem statement
Implement a JSON parser. It’s very unlikely that it’s something you’ll ever do (unless you’re writing your own programming language) and we certainly aren’t looking for compiler knowledge, but, from a modeling perspective, we’ve found it to be a nice way to force a problem with enough concepts and structure.

To sidestep some unnecessarily gnarly parts, let’s exclude:
* Non-integer numbers,
* Number exponents, and
* Unicode escape chars.

In our experience, this takes somewhere under 2 hours.

Example input
```
{
    "yes": true,
    "no": false,
    "nothing": null,
    "number": 123,
    "negative_number": -123,
    "strings": "A \"string\".\nFor real.",
    "object": {"omg": "things"},
    "list": [1, "a", {}, []]
}
```

Non-covered cases
```
{
    "floats": 7.54,
    "exponents": 10e100,
    "unicodes": "\u2603"
}
```
