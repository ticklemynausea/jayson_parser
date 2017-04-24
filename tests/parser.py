from lib.parser import Parser


sample = """
{
    "yes": true,
    "no": false,
    "nothing": null,
    "number": 123,
    "negative_number": -123,
    "strings": "A' string'.\nFor real.",
    "object": {"omg": "things"},
    "list": [1, "a", {}, []]
}
"""

p = Parser(sample)
result = p.parse()

print result, type(result)
