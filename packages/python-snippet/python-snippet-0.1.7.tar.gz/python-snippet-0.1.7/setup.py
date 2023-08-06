# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_snippet']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'decorator>=5.0.9,<6.0.0',
 'questionary>=1.9.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.4.0,<11.0.0',
 'textdistance>=4.2.1,<5.0.0',
 'typer-cli>=0.0.11,<0.0.12',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['python-snippet = python_snippet.main:app']}

setup_kwargs = {
    'name': 'python-snippet',
    'version': '0.1.7',
    'description': 'Python and Data Science Snippets on the command line',
    'long_description': '# Python Snippet Tool\n\nA tool to get Python and data science snippets at [Data Science Simplified](https://mathdatasimplified.com/) on the command line. You can read [my article](https://towardsdatascience.com/python-and-data-science-snippets-on-the-command-line-2673d5d9e55d) to learn how I created this tool.\n\n## Installation\n```bash\npython3 -m pip install --user python-snippet\n```\n**Note**: _The `--user` is important. It ensures you install it in your directory and not in the global system. `python3 -m` ensures that you install python_snippet using Python 3._\n\nMake sure your Python version is >= 3.6.2.\n```bash\npython3 --version\n```\n\n\n## Usage\n### Search for posts based on category\n![gif](https://github.com/khuyentran1401/python_snippet/blob/master/images/search_category2.gif?raw=true)\n\nYou can search for posts based on category by typing:\n```bash\npython-snippet search-category\n```\nOnce you select a post, you will receive an output like below:\n![image](https://github.com/khuyentran1401/python_snippet/blob/master/images/search_category2.png?raw=True)\n\n### Search for posts based on a string pattern\n![gif](https://github.com/khuyentran1401/python_snippet/blob/master/images/search_posts.gif?raw=true)\n\nYou can also search for posts using a string pattern such as `pandas`\n```bash\npython-snippet search-posts pandas\n```\n![image](https://github.com/khuyentran1401/python_snippet/blob/master/images/search_posts_pandas.png?raw=true)\n\nTo view all commands python-snippet provides, type:\n```bash\npython-snippet --help\n```\n![image](https://github.com/khuyentran1401/python_snippet/blob/master/images/help.png?raw=true)\n',
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/python_snippet.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
