Sphinx Code Highlighter Directive
=================================

A Sphinx directive that works just like a code-block plus allows you to
highlight partial lines.

Examples
--------

Using [MyST markdown](https://myst-parser.readthedocs.io/en/latest/using/syntax.html):

`````markdown

```{code-block-hl} python
:linenos:
:caption: "The text surrounded by `!!!` gets highlighted."
dwarves = [
  "Bashful",
  "Dopey",
  "Happy",
  "Grumpy",
  "Sleepy",
  "Sneezy",
  "Doc",
]

i = 0
while i < len(!!!dwarves!!!):
  !!!name!!! = dwarves[i]
  print(f"{name}s Room")
  i += 1
```

`````

![screenshot](docs/img/alabaster-demo.png)
