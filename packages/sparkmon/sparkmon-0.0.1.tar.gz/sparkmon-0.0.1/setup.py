# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sparkmon']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'data-science-types',
 'ipython',
 'matplotlib',
 'pandas',
 'pandas-stubs',
 'psutil',
 'pyspark',
 'urlpath']

entry_points = \
{'console_scripts': ['sparkmon = sparkmon.__main__:main']}

setup_kwargs = {
    'name': 'sparkmon',
    'version': '0.0.1',
    'description': 'sparkmon',
    'long_description': "sparkmon\n========\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/sparkmon.svg\n   :target: https://pypi.org/project/sparkmon/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/sparkmon\n   :target: https://pypi.org/project/sparkmon\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/sparkmon\n   :target: https://opensource.org/licenses/Apache-2.0\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/sparkmon/latest.svg?label=Read%20the%20Docs\n   :target: https://sparkmon.readthedocs.io/\n   :alt: Read the documentation at https://sparkmon.readthedocs.io/\n.. |Tests| image:: https://github.com/stephanecollot/sparkmon/workflows/Tests/badge.svg\n   :target: https://github.com/stephanecollot/sparkmon/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/stephanecollot/sparkmon/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/stephanecollot/sparkmon\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\nMonitoring plot example:\n\n.. image:: docs/images/monitoring-plot-example.png\n\n* Logs the executors metrics\n* Create a monitoring thread directly in your PySpark application\n* Plot monitoring for a remote Spark application in a notebook, or in a file\n* Command line interface for a remote Spark application\n\n\nRequirements\n------------\n\n* Python\n* Spark\n\n\nInstallation\n------------\n\nYou can install *sparkmon* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install sparkmon\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `Apache 2.0 license`_,\n*sparkmon* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _Apache 2.0 license: https://opensource.org/licenses/Apache-2.0\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/stephanecollot/sparkmon/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://sparkmon.readthedocs.io/en/latest/usage.html\n",
    'author': 'Stephane Collot',
    'author_email': 'stephane.collot@ing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephanecollot/sparkmon',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
