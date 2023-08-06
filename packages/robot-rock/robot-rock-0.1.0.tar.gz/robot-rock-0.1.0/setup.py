# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robot_rock']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=4.5.0,<5.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['robot-rock = robot_rock:app']}

setup_kwargs = {
    'name': 'robot-rock',
    'version': '0.1.0',
    'description': '',
    'long_description': "# `robot`\n\nThis is a command line application implementation of Victor Nguyen's [toy robot problem](https://github.com/victornguyen/toy-robot/blob/e9805881e99bd83b27f4b57a857730f526cd7669/README.md) in Python.\n\n## Installation\n\nThe best way to install `robot` is via [pipx](https://github.com/pypa/pipx#install-pipx), which will isolate the installation but make the app available globally:\n\n```console\n$ pipx install robot-rock\n```\n\nAlternatively, you can create your own virtual environment:\n\n```console\n$ python3 -m venv .venv-robot --prompt robot-rock\n```\n\nAnd then activate the virtual environment and install the app with vanilla pip:\n\n```console\n$ source .venv-robot/bin/activate\n(robot-rock)$ pip install --user robot-rock\n```\n\n## Usage:\n\n```console\n$ robot [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n- `--help`: Show this message and exit.\n\n**Commands**:\n\n- `left`: Rotate the robot counterclockwise 90 degress.\n- `move`: Move the robot forward one square, without falling off the eboard.\n- `place`: Place the robot on the board.\n- `report`: Report the robot's position on the board.\n- `right`: Rotate the robot clockwise 90 degress.\n- `rock`: Rock out with the robot.\n\n## `robot left`\n\nRotate the robot counterclockwise 90 degress.\n\n**Usage**:\n\n```console\n$ robot left\n```\n\n## `robot move`\n\nMove the robot forward one square, without falling off the board.\n\n**Usage**:\n\n```console\n$ robot move\n```\n\n## `robot place`\n\nPlace the robot on the board.\n\nType X,Y,F with no spaces, where X is the x-coordinate,\nY is the y-coordinate, and F is the direction the robot\nis facing (NORTH, SOUTH, EAST, or WEST).\n\n**Usage**:\n\n```console\n$ robot place PLACEMENT\n```\n\n**Arguments**:\n\n- `PLACEMENT`: [required]\n\n## `robot report`\n\nReport the robot's position on the board.\n\n**Usage**:\n\n```console\n$ robot report\n0,1,NORTH\n```\n\n## `robot right`\n\nRotate the robot clockwise 90 degress.\n\n**Usage**:\n\n```console\n$ robot right\n```\n\n## `robot rock`\n\nRock out with the robot :robot: :metal:.\n\n**Usage**:\n\n```console\n$ robot rock\n```\n",
    'author': 'Oliver Josem',
    'author_email': 'omjosem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
