# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['instmuse']

package_data = \
{'': ['*']}

install_requires = \
['numuse>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'instmuse',
    'version': '0.1.2',
    'description': 'Physical instrument library',
    'long_description': "# Instmuse\n\nThis package is a set of tools designed to work with physical instruments, it uses numuse's notation.\n\nTo get started visit the [documentation](https://instmuse.readthedocs.io/en/latest/).\n\nIf you're able to find use in this project, then please consider [contributing](https://www.patreon.com/cuppajoeman).\n",
    'author': 'ccn',
    'author_email': 'ccn@cuppajoeman.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/cuppajoeman/instmuse',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
