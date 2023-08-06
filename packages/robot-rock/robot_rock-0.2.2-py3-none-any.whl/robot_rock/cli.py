import typer

from robot_rock import Robot

app = typer.Typer(add_completion=False)


@app.command()
def place(placement: str):
    """
    Place the robot on the board.

    Type X,Y,F with no spaces, where X is the x-coordinate,
    Y is the y-coordinate, and F is the direction the robot
    is facing (NORTH, SOUTH, EAST, or WEST).
    """
    Robot.place(placement)


@app.command()
def move():
    """
    Move the robot forward one square, without falling off the board.
    """
    Robot.move()


@app.command()
def left():
    """
    Rotate the robot counterclockwise 90 degress.
    """
    Robot.rotate("LEFT")


@app.command()
def right():
    """
    Rotate the robot clockwise 90 degress.
    """
    Robot.rotate("RIGHT")


@app.command()
def report():
    """
    Report the robot's position on the board.
    """
    Robot.report()


@app.command()
def rock():
    """
    Rock out with the robot.
    """
    typer.echo("🤖🤘")
