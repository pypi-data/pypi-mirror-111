# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycharmers',
 'pycharmers.cli',
 'pycharmers.matplotlib',
 'pycharmers.opencv',
 'pycharmers.sdk',
 'pycharmers.utils']

package_data = \
{'': ['*'], 'pycharmers': ['templates/*', 'templates/_macros/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'Pillow>=8.2.0,<9.0.0',
 'PyDrive>=1.3.1,<2.0.0',
 'PyMuPDF>=1.18.13,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'camelot-py>=0.8.2,<0.9.0',
 'html5lib>=1.1,<2.0',
 'lxml>=4.6.3,<5.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'mysqlclient>=2.0.3,<3.0.0',
 'nptyping>=1.4.2,<2.0.0',
 'numpy-stl>=2.16.0,<3.0.0',
 'numpy>=1.20.3,<2.0.0',
 'opencv-contrib-python>=4.5.2,<5.0.0',
 'paramiko>=2.7.2,<3.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-xlib>=0.29,<0.30',
 'requests>=2.25.1,<3.0.0',
 'scipy==1.4.1',
 'scp>=0.13.3,<0.14.0',
 'selenium>=3.141.0,<4.0.0',
 'wcwidth>=0.2.5,<0.3.0']

entry_points = \
{'console_scripts': ['book2img = pycharmers.cli.book2img:book2img',
                     'cv-cascades = pycharmers.cli.cvCascades:cvCascades',
                     'cv-paper-scanner = '
                     'pycharmers.cli.cvPaperScanner:cvPaperScanner',
                     'cv-pencil-sketch = '
                     'pycharmers.cli.cvPencilSketch:cvPencilSketch',
                     'cv-window = pycharmers.cli.cvWindow:cvWindow',
                     'form-auto-fill-in = '
                     'pycharmers.cli.form_auto_fill_in:form_auto_fill_in',
                     'jupyter-arrange = '
                     'pycharmers.cli.jupyter_arrange:jupyter_arrange',
                     'openBrowser = pycharmers.cli.openBrowser:openBrowser',
                     'pdfmine = pycharmers.cli.pdfmine:pdfmine',
                     'pycharmers-show = '
                     'pycharmers.cli.show:show_command_line_programs',
                     'regexp-replacement = '
                     'pycharmers.cli.regexp_replacement:regexp_replacement',
                     'render-template = '
                     'pycharmers.cli.render_template:render_template',
                     'requirements-create = '
                     'pycharmers.cli.requirements:requirements_create',
                     'revise_text = pycharmers.cli.revise_text:revise_text',
                     'tweetile = pycharmers.cli.tweetile:tweetile',
                     'video2gif = pycharmers.cli.video2gif:video2gif',
                     'video_of_lyric = '
                     'pycharmers.cli.video_of_lyric:video_of_lyric',
                     'video_of_typing = '
                     'pycharmers.cli.video_of_typing:video_of_typing']}

setup_kwargs = {
    'name': 'pycharmers',
    'version': '0.2.0',
    'description': 'A collection of useful python programs.',
    'long_description': '# Python-Charmers\n\n[![header](https://github.com/iwasakishuto/Python-Charmers/blob/master/image/header.png?raw=true)](https://github.com/iwasakishuto/Python-Charmers)\n[![PyPI version](https://badge.fury.io/py/Python-Charmers.svg)](https://pypi.org/project/Python-Charmers/)\n[![GitHub version](https://badge.fury.io/gh/iwasakishuto%2FPython-Charmers.svg)](https://github.com/iwasakishuto/Python-Charmers)\n[![Execute Python-Charmers](https://github.com/iwasakishuto/Python-Charmers/actions/workflows/execute_python_package.yml/badge.svg)](https://github.com/iwasakishuto/Python-Charmers/actions/workflows/execute_python_package.yml)\n[![Upload to PyPI with Poetry](https://github.com/iwasakishuto/Python-Charmers/actions/workflows/upload_python_package_poetry.yml/badge.svg)](https://github.com/iwasakishuto/Python-Charmers/actions/workflows/upload_python_package_poetry.yml)\n[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/iwasakishuto/Python-Charmers/blob/master/LICENSE)\n\nA collection of useful python programs.\n\n## Installation\n\n1. Install **MySQL**\n\t- **Debian/Ubuntu**\n\t\t```sh\n\t\t$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential\n\t\t```\n\t- **Red Hat/Cent OS**\n\t\t```sh\n\t\t% sudo yum install python3-devel mysql-devel\n\t\t```\n\t- **macOS**\n\t\t```sh\n\t\t# Install MySQL server\n\t\t$ brew install mysql\n\t\t# If you don\'t want to install MySQL server, you can use mysql-client instead:\n\t\t$ brew install mysql-client\n\t\t$ echo \'export PATH="/usr/local/opt/mysql-client/bin:$PATH"\' >> ~/.zprofile\n\t\t$ export PATH="/usr/local/opt/mysql-client/bin:$PATH"\n\t\t```\n2. Install **`Python-Charmers`** (There are two ways to install):\n\t-  Create an environment for Python-Charmers using [Pyenv](https://github.com/pyenv/pyenv) and [Poetry](https://python-poetry.org/) **(recommended)**\n\t\t```sh\n\t\t$ pyenv install 3.8.9\n\t\t$ pyenv local 3.8.9\n\t\t$ python -V\n\t\tPython 3.8.9\n\t\t$ poetry install\n\t\t```\n\t-  Install in a specific environment\n\t\t-  Install from PyPI:\n\t\t\t```sh\n\t\t\t$ sudo pip install Python-Charmers\n\t\t\t```\n\t\t-  Alternatively: install PyGuitar from the GitHub source:\n\t\t\t```sh            \n\t\t\t$ git clone https://github.com/iwasakishuto/Python-Charmers.git\n\t\t\t# If you want to use the latest version (under development)\n\t\t\t$ git clone -b develop https://github.com/iwasakishuto/Python-Charmers.git\n\t\t\t$ cd Python-Charmers\n\t\t\t$ sudo python setup.py install\n\t\t\t```\n3. Install **driver** for `selenium`:\n**`Selenium`** requires a driver to interface with the chosen browser, so please visit the [documentation](https://selenium-python.readthedocs.io/installation.html#drivers) to install it.\n\t```sh\n\t# Example: Chrome\n\t# visit "chrome://settings/help" to check your chrome version.\n\t# visit "https://chromedriver.chromium.org/downloads" to check <Suitable.Driver.Version> for your chrome.\n\t$ wget https://chromedriver.storage.googleapis.com/<Suitable.Driver.Version>/chromedriver_mac64.zip\n\t$ unzip chromedriver_mac64.zip\n\t$ mv chromedriver /usr/local/bin/chromedriver\n\t$ chmod +x /usr/local/bin/chromedriver\n\t```\n\n### Pyenv + Poetry\n\n- [Pyenv](https://github.com/pyenv/pyenv) is a python installation manager.\n- [Poetry](https://python-poetry.org/) is a packaging and dependency manager.\n\nI recommend you to use these tools to **avoid the chaos** of the python environment. See other sites for how to install these tools.\n\n```sh\n$ pyenv install 3.8.9\n$ pyenv local 3.8.9\n$ python -V\nPython 3.8.9\n$ poetry install \n$ poetry run pycharmers-show\n$ poetry run book2img\n```\n\n## CLI\n\n**CLI** is a command line program that accepts text input to execute operating system functions.\n\n```sh\n# If you use Poetry to set up the environment.\n$ poetry run pycharmers-show\n|       command       |                         path                         |\n|:-------------------:|:-----------------------------------------------------|\n|            book2img | pycharmers.cli.book2img:book2img                     |\n|         cv-cascades | pycharmers.cli.cvCascades:cvCascades                 |\n|               :     |              :                                       |\n|            tweetile | pycharmers.cli.tweetile:tweetile                     |\n|           video2gif | pycharmers.cli.video2gif:video2gif                   |\n```\n\n|                                                                              command                                                                               |                                   description                                                                                                             |\n|:------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|\n|                                         [`book2img`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.book2img.html#pycharmers.cli.book2img.book2img) | Convert Book into Sequential Images.                                                                                                                      |\n|                                [`cv-cascades`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.cvCascades.html#pycharmers.cli.cvCascades.cvCascades) | Control the OpenCV cascade Examples.                                                                                                                      |\n|               [`cv-paper-scanner`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.cvPaperScanner.html#pycharmers.cli.cvPaperScanner.cvPaperScanner) | Paper Scanner using OpenCV.                                                                                                                               |\n|               [`cv-pencil-sketch`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.cvPencilSketch.html#pycharmers.cli.cvPencilSketch.cvPencilSketch) | Convert the image like a pencil drawing.                                                                                                                  |\n|                                        [`cv-window`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.cvWindow.html#pycharmers.cli.cvWindow.cvWindow) | Use [`cvWindow`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.opencv.windows.html#pycharmers.opencv.windows.cvWindow) to control frames.     |\n|     [`form-auto-fill-in`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.form_auto_fill_in.html#pycharmers.cli.form_auto_fill_in.form_auto_fill_in) | Auto fill in your form using your saved information (or answer on the spot).                                                                              |\n|             [`jupyter-arrange`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.jupyter_arrange.html#pycharmers.cli.jupyter_arrange.jupyter_arrange) | Arrange Jupyter Notebook.                                                                                                                                 |\n|                             [`openBrowser`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.openBrowser.html#pycharmers.cli.openBrowser.openBrowser) | Display url using the default browser.                                                                                                                    |\n|                                             [`pdfmine`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.pdfmine.html#pycharmers.cli.pdfmine.pdfmine) | Analyze PDF and extract various elements.                                                                                                                 |\n| [`regexp-replacement`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.regexp_replacement.html#pycharmers.cli.regexp_replacement.regexp_replacement) | String replacement in a file using regular expression                                                                                                     |\n|             [`render-template`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.render_template.html#pycharmers.cli.render_template.render_template) | Render templates.                                                                                                                                         |\n|           [`requirements-create`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.requirements.html#pycharmers.cli.requirements.requirements_create) | Create a ``requirements.text``                                                                                                                            |\n|                             [`revise_text`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.revise_text.html#pycharmers.cli.revise_text.revise_text) | Revise word file.                                                                                                                                         |\n|                        [`pycharmers-show`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.show.html#pycharmers.cli.show.show_command_line_programs) | Show all Python-Charmers\'s command line programs.                                                                                                         |\n|                                         [`tweetile`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.tweetile.html#pycharmers.cli.tweetile.tweetile) | Divide one image into three so that you can tweet beautifully.                                                                                            |\n|                 [`video_of_lyric`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.video_of_lyric.html#pycharmers.cli.video_of_lyric.video_of_lyric) | Create a lyric Video.                                                                                                                                     |\n|             [`video_of_typing`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.video_of_typing.html#pycharmers.cli.video_of_typing.video_of_typing) | Create a typing video. Before using this program, please do the following things                                                                          |\n|                                     [`video2gif`](https://iwasakishuto.github.io/Python-Charmers/pycharmers.cli.video2gif.html#pycharmers.cli.video2gif.video2gif) | Convert Video into Gif.                                                                                                                                   |',
    'author': 'iwasakishuto',
    'author_email': 'cabernet.rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iwasakishuto.github.io/Python-Charmers/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
