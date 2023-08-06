# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quick_pdf']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['quickpdf_merge = quick_pdf.merge:merge_pdf']}

setup_kwargs = {
    'name': 'quick-pdf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vibhu Agarwal',
    'author_email': 'vibhu4agarwal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
