# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_highlighter']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.9.0,<3.0.0', 'Sphinx>=3,<4']

setup_kwargs = {
    'name': 'sphinx-code-highlighter',
    'version': '0.0.2',
    'description': 'code-block-hl directive, just like code-block but with partial line highlights',
    'long_description': 'Sphinx Code Highlighter Directive\n=================================\n\nA Sphinx directive that works just like a code-block plus allows you to\nhighlight partial lines.\n\nExamples\n--------\n\nUsing [MyST markdown](https://myst-parser.readthedocs.io/en/latest/using/syntax.html):\n\n`````markdown\n\n```{code-block-hl} python\n:linenos:\n:caption: "The text surrounded by `!!!` gets highlighted."\ndwarves = [\n  "Bashful",\n  "Dopey",\n  "Happy",\n  "Grumpy",\n  "Sleepy",\n  "Sneezy",\n  "Doc",\n]\n\ni = 0\nwhile i < len(!!!dwarves!!!):\n  !!!name!!! = dwarves[i]\n  print(f"{name}s Room")\n  i += 1\n```\n\n`````\n\n![screenshot](docs/img/alabaster-demo.png)\n',
    'author': 'Alissa Huskey',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alissa-huskey/sphinx-code-highlighter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
