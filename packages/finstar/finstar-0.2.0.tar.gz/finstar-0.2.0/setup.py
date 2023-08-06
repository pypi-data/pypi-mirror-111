# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['finstar', 'finstar.evaluation', 'finstar.strategies']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas-market-calendars>=2.0,<3.0',
 'pandas>=1.2.4,<2.0.0',
 'pyarrow>=4.0.1,<5.0.0',
 'yfinance>=0.1.59,<0.2.0']

setup_kwargs = {
    'name': 'finstar',
    'version': '0.2.0',
    'description': 'Modeling financial time series. WIP!',
    'long_description': '# finstar\n\n🚧 WIP 🚧\n\n## Installation\n\n```\npoetry install\npoetry run pre-commit install\n```\n\n### Serving documentation\n\n```\npoetry run mkdocs serve\n```\n\n## Development\n\n### Testing\n\n```\npoetry run pytest\n```\n\n### Bumping version\n\n```\npoetry run bump2version minor # major or minor or patch\ngit-push --tags\n```\n\n### Publication to PyPI\n\n```\npoetry build\npoetry publish\n```\n\n### tox\n\n```\n poetry run tox\n ```\n',
    'author': 'Alexander Junge',
    'author_email': 'alexander.junge@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JungeAlexander/finstar',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
