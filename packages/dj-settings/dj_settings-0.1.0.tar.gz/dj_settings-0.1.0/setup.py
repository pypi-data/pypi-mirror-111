# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dj_settings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dj-settings',
    'version': '0.1.0',
    'description': 'django settings manager',
    'long_description': '<p align="center">\n<a href="https://www.travis-ci.com/spapanik/dj_settings"><img alt="Build" src="https://www.travis-ci.com/spapanik/dj_settings.svg?branch=main"></a>\n<a href="https://github.com/spapanik/dj_settings/blob/main/LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/spapanik/dj_settings"></a>\n<a href="https://pypi.org/project/dj_settings"><img alt="PyPI" src="https://img.shields.io/pypi/v/dj_settings"></a>\n<a href="https://pepy.tech/project/dj_settings"><img alt="Downloads" src="https://pepy.tech/badge/dj_settings"></a>\n<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/dj_settings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
