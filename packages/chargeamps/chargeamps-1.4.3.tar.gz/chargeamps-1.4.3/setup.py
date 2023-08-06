# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chargeamps']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7.1,<2.0.0',
 'aiohttp>=3.7.2,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'isodate>=0.6.0,<0.7.0',
 'marshmallow>=3.9.0,<4.0.0']

entry_points = \
{'console_scripts': ['chargeamps = chargeamps.cli:main']}

setup_kwargs = {
    'name': 'chargeamps',
    'version': '1.4.3',
    'description': 'Charge-Amps API bindings for Python',
    'long_description': "# Charge Amps API bindings for Python\n\nThis repository contains a Python module for the Charge Amps' electric vehicle charging stations.\n\nThe module is developed by [Kirei AB](https://www.kirei.se) and is not supported by [Charge Amps AB](https://charge-amps.com).\n\n\n## External API Key\n\nYou need an API key to use the Charge Amps external API. Contact [Charge Amps Support](mailto:support@charge-amps.com) for extensive API documentation and API key.\n\n\n## References\n\n- [Charge Amps External REST API](https://ca-externalapi.azurewebsites.net/swagger/)\n",
    'author': 'Jakob Schlyter',
    'author_email': 'jakob@kirei.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kirei/python-chargeamps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
