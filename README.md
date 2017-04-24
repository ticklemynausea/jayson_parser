# jayson Parser

Because normal json is too good for me.

# What is this?

Not json. See `PROBLEM.md`.

## What to do with this?

* Read and run the unit tests:
```
$ python -m unittest tests.tokenizer.TestTokenizer
```
```
$ python -m unittest tests.parser.TestParser
```
(you probably don't really care much for the tokenizer as it's just an intermediate step, but hey, it's there)

* Fiddle around with the demo in `demo.py`. In it I used the parser to do some real processing with a **jayson** string.

```
$ python demo.py
```


## TODO:

* Deal explicitly with object key uniqueness. Keys that appear more than once just have their values overwritten as the parser does its thing.

* Handle invalid input more gracefully, as well as add tests to ensure that invalid input results in
expected failures.

## Notes:

* The problem statement has a string with nested quotes: `"A \"string\".\nFor real."`. In python,
string literals like these need to be prefixed with an `r`, like `r"A \"string\".\nFor real."`. Otherwise,
the backslash will end up being treated as an escape character. This is relevant if you're reading the unit tests, you will notice some strings have the `r` prefix while others don't.
