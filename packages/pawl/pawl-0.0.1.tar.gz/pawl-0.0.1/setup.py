# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pawl', 'pawl.core', 'pawl.service', 'pawl.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pawl',
    'version': '0.0.1',
    'description': "PAWL (an acronym for `Python API Wrapper - LinkedIn`) allows for simple access to LinkedIn's API.",
    'long_description': '# PAWL: Python API Wrapper for LinkedIn\n\nOAuth flow will be added in the next revision.\n\n## Installation\n\nPAWL is supported on Python 3.9+. The recommended way to install PAWL is with pip.\n\n`pip install pawl`\n\n## Quickstart\n\nYou can instantiate an instance like so:\n\n```python\nimport pawl\n\n>>> linkedin = pawl.Linkedin(\n    access_token="ACCESS_TOKEN_VALUE",\n)\n\n>>> linkedin\n<pawl.linkedin.Linkedin at 0x10ea46af0>\n```\n\n#### get_basic_profile()\n```python\n>>> response = linkedin.me.get_basic_profile()\n\n>>> response\n{\n    \'localizedLastName\': \'LAST_NAME\',\n    \'profilePicture\': {\n        \'displayImage\': \'urn:li:digitalmediaAsset:PHOTO_ID_VALUE\'\n    },\n    \'firstName\': {\n        \'localized\': {\n            \'language_code_value_and_country_code_value\': \'FIRST_NAME_VALUE\'\n        },\n        \'preferredLocale\': {\n            \'country\': \'country_code_value\', \'language\': \'language_code_value\'\n        }\n    },\n    \'lastName\': {\n        \'localized\': {\n            \'language_code_value_and_country_code_value\':\n            \'LAST_NAME_VALUE\'\n        },\n        \'preferredLocale\': {\n            \'country\': \'country_code_value\',\n            \'language\': \'language_value\'\n        }\n    },\n    \'id\': \'USER_ID_VALUE\',\n    \'localizedFirstName\': \'localized_first_name_value\'\n}\n```\n\n## License\n\nPAWL\'s source is provided under the MIT License.\n\n- Copyright © 2021 Kyle J. Burda\n',
    'author': 'Kyle J. Burda',
    'author_email': 'kylejbdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
