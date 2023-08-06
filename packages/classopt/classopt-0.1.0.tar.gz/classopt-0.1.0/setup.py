# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classopt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'classopt',
    'version': '0.1.0',
    'description': 'Arguments parser with class for Python, inspired by StructOpt',
    'long_description': '<h1 align="center">Welcome to ClassOpt 👋</h1>\n<p>\n  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />\n  <a href="https://github.com/moisutsu/classopt/blob/main/LICENSE" target="_blank">\n    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />\n  </a>\n  <a href="https://twitter.com/moisutsu" target="_blank">\n    <img alt="Twitter: moisutsu" src="https://img.shields.io/twitter/follow/moisutsu.svg?style=social" />\n  </a>\n</p>\n\n> Arguments parser with class for Python, inspired by [StructOpt](https://github.com/TeXitoi/structopt)\n\n## Install\n\n```sh\npip install classopt\n```\n\n## Usage\n\nImport `ClassOpt` and define the Opt class with decorator.\n\n```python\nfrom classopt import ClassOpt\n\n@ClassOpt\nclass Opt:\n    arg_int: int\n    arg_str: str\n\nif __name__ == "__main__":\n  opt = Opt.from_args()\n  print(opt.arg_int, opt.arg_str)\n```\n\nRun with command line arguments.\n\n```bash\n$ python main.py --arg_int 5 --arg_str hello\n5 hello\n```\n\n\n\n## Run tests\n\n```sh\npoetry run pytest\n```\n\n## Author\n\n👤 **moisutsu**\n\n* Twitter: [@moisutsu](https://twitter.com/moisutsu)\n* Github: [@moisutsu](https://github.com/moisutsu)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\n## 📝 License\n\nCopyright © 2021 [moisutsu](https://github.com/moisutsu).<br />\nThis project is [MIT](https://github.com/moisutsu/classopt/blob/main/LICENSE) licensed.\n\n***\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'moisutsu',
    'author_email': 'moisutsu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moisutsu/classopt',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
