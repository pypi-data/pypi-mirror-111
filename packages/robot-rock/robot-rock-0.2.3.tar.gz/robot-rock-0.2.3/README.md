# `robot-rock`

This is a command line application implementation of Victor Nguyen's [toy robot problem](https://github.com/victornguyen/toy-robot/blob/e9805881e99bd83b27f4b57a857730f526cd7669/README.md) in Python.

## Installation

`robot-rock` requires Python 3.7 or above.

The best way to install `robot-rock` is via [pipx](https://github.com/pypa/pipx#install-pipx), which will isolate the installation but make the app available globally:

```console
$ pipx install robot-rock
```

Alternatively, you can create your own virtual environment:

```console
$ python3 -m venv .venv-robot --prompt robot-rock
```

And then activate the virtual environment and install the app with vanilla pip:

```console
$ source .venv-robot/bin/activate
(robot-rock)$ pip install robot-rock
```

## Usage:

```console
$ robot-rock [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `left`: Rotate the robot counterclockwise 90 degress.
- `move`: Move the robot forward one square, without falling off the board.
- `place`: Place the robot on the board.
- `report`: Report the robot's position on the board.
- `right`: Rotate the robot clockwise 90 degress.
- `rock`: Rock out with the robot.

## `robot-rock left`

Rotate the robot counterclockwise 90 degress.

**Usage**:

```console
$ robot-rock left
```

## `robot-rock move`

Move the robot forward one square, without falling off the board.

**Usage**:

```console
$ robot-rock move
```

## `robot-rock place`

Place the robot on the board.

Type X,Y,F with no spaces, where X is the x-coordinate,
Y is the y-coordinate, and F is the direction the robot
is facing (NORTH, SOUTH, EAST, or WEST).

**Usage**:

```console
$ robot-rock place PLACEMENT
```

**Arguments**:

- `PLACEMENT`: [required]

## `robot-rock report`

Report the robot's position on the board.

**Usage**:

```console
$ robot-rock report
0,1,NORTH
```

## `robot-rock right`

Rotate the robot-rock clockwise 90 degress.

**Usage**:

```console
$ robot-rock right
```

## `robot-rock rock`

Rock out with the robot :robot: :metal:.

**Usage**:

```console
$ robot-rock rock
```
