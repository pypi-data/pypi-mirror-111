# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deezer', 'deezer.contrib']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.18,<3.0']

extras_require = \
{'docs': ['myst-parser>=0.15,<0.16',
          'sphinx>=4,<5',
          'sphinx-autobuild>=2021.0.0,<2022.0.0',
          'sphinx-rtd-theme>=0.5,<0.6'],
 'tornado': ['tornado>=6.0.4,<7.0.0']}

setup_kwargs = {
    'name': 'deezer-python',
    'version': '2.3.0',
    'description': 'A friendly wrapper library for the Deezer API',
    'long_description': 'Deezer Python Client\n====================\n\n<p align="center">\n  <a href="https://github.com/browniebroke/deezer-python/actions?query=workflow%3ACI">\n    <img alt="CI Status" src="https://img.shields.io/github/workflow/status/browniebroke/deezer-python/CI?label=CI&logo=github&style=flat-square">\n  </a>\n  <a href="https://deezer-python.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/deezer-python.svg?logo=read-the-docs&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/browniebroke/deezer-python">\n    <img src="https://img.shields.io/codecov/c/github/browniebroke/deezer-python.svg?logo=codecov&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://mybinder.org/v2/gh/browniebroke/deezer-python/main?filepath=demo.ipynb">\n    <img src="https://mybinder.org/badge_logo.svg" alt="Launch demo on Binder">\n  </a>\n  <a href="https://pypi.org/project/deezer-python/">\n    <img src="https://img.shields.io/pypi/v/deezer-python.svg?logo=python&amp;logoColor=fff&amp;style=flat-square" alt="PyPi Status">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/deezer-python.svg?style=flat-square" alt="pyversions">\n  <img src="https://img.shields.io/pypi/l/deezer-python.svg?style=flat-square" alt="license">\n  <a href="https://github.com/browniebroke/deezer-python">\n    <img src="https://tokei.rs/b1/github/browniebroke/deezer-python/" alt="LoC">\n  </a>\n</p>\n\nA friendly Python wrapper around the [Deezer API](http://developers.deezer.com/api).\n\nInstallation\n------------\n\nThe package is published on\n[PyPI](https://pypi.org/project/deezer-python/) and can be installed by running:\n\n    pip install deezer-python\n\nBasic Use\n---------\n\nEasily query the Deezer API from you Python code. The data returned by the Deezer\nAPI is mapped to python resources:\n\n```python\n>>> client = deezer.Client()\n>>> client.get_album(680407).title\n\'Monkey Business\'\n```\n\nReady for more? Look at our whole [documentation](http://deezer-python.readthedocs.io/)\non Read The Docs or have a play in pre-populated Jupyter notebook\n[on Binder](https://mybinder.org/v2/gh/browniebroke/deezer-python/main?filepath=demo.ipynb).\n\n\nContributors\n------------\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://www.twitter.com/_BrunoAlla"><img src="https://avatars1.githubusercontent.com/u/861044?v=4" width="100px;" alt=""/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=browniebroke" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=browniebroke" title="Documentation">📖</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-browniebroke" title="Maintenance">🚧</a> <a href="#platform-browniebroke" title="Packaging/porting to new platform">📦</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=browniebroke" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/misuzu"><img src="https://avatars1.githubusercontent.com/u/248143?v=4" width="100px;" alt=""/><br /><sub><b>misuzu</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=misuzu" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=misuzu" title="Documentation">📖</a> <a href="#ideas-misuzu" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=misuzu" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/pfouque"><img src="https://avatars1.githubusercontent.com/u/8300001?v=4" width="100px;" alt=""/><br /><sub><b>Pascal</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=pfouque" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=pfouque" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/khamaileon"><img src="https://avatars2.githubusercontent.com/u/1322166?v=4" width="100px;" alt=""/><br /><sub><b>khamaileon</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=khamaileon" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/sheregeda"><img src="https://avatars3.githubusercontent.com/u/2856444?v=4" width="100px;" alt=""/><br /><sub><b>Nikolay Sheregeda</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=sheregeda" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=sheregeda" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/horstmannmat"><img src="https://avatars1.githubusercontent.com/u/11761333?v=4" width="100px;" alt=""/><br /><sub><b>Matheus Horstmann</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=horstmannmat" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=horstmannmat" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/MDCEY"><img src="https://avatars2.githubusercontent.com/u/3812864?v=4" width="100px;" alt=""/><br /><sub><b>Kieran Wynne</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=MDCEY" title="Code">💻</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="https://github.com/jnth"><img src="https://avatars0.githubusercontent.com/u/7796167?v=4" width="100px;" alt=""/><br /><sub><b>Jonathan Virga</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=jnth" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=jnth" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/hugovk"><img src="https://avatars2.githubusercontent.com/u/1324225?v=4" width="100px;" alt=""/><br /><sub><b>Hugo</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=hugovk" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/all-contributors/all-contributors-bot"><img src="https://avatars3.githubusercontent.com/u/46843839?v=4" width="100px;" alt=""/><br /><sub><b>allcontributors[bot]</b></sub></a><br /><a href="#infra-allcontributors" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>\n    <td align="center"><a href="https://github.com/nrebena"><img src="https://avatars3.githubusercontent.com/u/49879400?v=4" width="100px;" alt=""/><br /><sub><b>nrebena</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/issues?q=author%3Anrebena" title="Bug reports">🐛</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=nrebena" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=nrebena" title="Tests">⚠️</a></td>\n    <td align="center"><a href="https://github.com/spvkgn"><img src="https://avatars0.githubusercontent.com/u/4147135?v=4" width="100px;" alt=""/><br /><sub><b>Pavel</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/issues?q=author%3Aspvkgn" title="Bug reports">🐛</a></td>\n    <td align="center"><a href="http://www.idiap.ch || www.edeltech.ch"><img src="https://avatars0.githubusercontent.com/u/898010?v=4" width="100px;" alt=""/><br /><sub><b>Samuel Gaist</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=sgaist" title="Code">💻</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=sgaist" title="Tests">⚠️</a> <a href="#security-sgaist" title="Security">🛡️</a></td>\n    <td align="center"><a href="https://github.com/hithomasmorelli"><img src="https://avatars0.githubusercontent.com/u/22722644?v=4" width="100px;" alt=""/><br /><sub><b>Thomas Morelli</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/issues?q=author%3Ahithomasmorelli" title="Bug reports">🐛</a> <a href="https://github.com/browniebroke/deezer-python/commits?author=hithomasmorelli" title="Code">💻</a> <a href="#ideas-hithomasmorelli" title="Ideas, Planning, & Feedback">🤔</a></td>\n  </tr>\n  <tr>\n    <td align="center"><a href="https://naveen.syrusdark.website"><img src="https://avatars1.githubusercontent.com/u/49693820?v=4" width="100px;" alt=""/><br /><sub><b>Naveen M K</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-python/commits?author=naveen521kk" title="Code">💻</a> <a href="#infra-naveen521kk" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-enable -->\n<!-- prettier-ignore-end -->\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://allcontributors.org) specification.\nContributions of any kind are welcome!\n',
    'author': 'Bruno Alla',
    'author_email': 'alla.brunoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/browniebroke/deezer-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
