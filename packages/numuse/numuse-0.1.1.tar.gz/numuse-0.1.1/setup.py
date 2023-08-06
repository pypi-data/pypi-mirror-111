# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['numuse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'numuse',
    'version': '0.1.1',
    'description': 'Music experimentation library',
    'long_description': "# Numuse\n\nThis package is a set of tools designed for the analysis of music, it uses notation that connects with the code and fundamental building blocks of music.\n\nTo get started visit the [documentation](https://numuse.readthedocs.io/en/latest/).\n\nIf you're able to find use in this project, then please consider [contributing](https://www.patreon.com/cuppajoeman).\n",
    'author': 'ccn',
    'author_email': 'ccn@cuppajoeman.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/cuppajoeman/numuse',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
