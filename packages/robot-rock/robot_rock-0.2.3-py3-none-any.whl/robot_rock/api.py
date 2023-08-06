import os
import sys
from contextlib import contextmanager

from tinydb import TinyDB, table
from tinydb.operations import decrement, increment

__all__ = ["Robot"]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, "db.json")


@contextmanager
def robot_db(db_path):
    db = TinyDB(db_path)
    yield db
    db.close()


def validate_coordinate(coord):
    """Check the coordinates input by the user are integers between 0 and 4."""
    try:
        coord = int(coord)
        if coord >= 0 and coord <= 4:
            return coord
    except:
        print("Position must be between 0 and 4.")
        sys.exit(1)


def validate_facing(facing):
    """Check the direction the user turned the robot to face is valid."""
    if (facing := facing.upper()) in ("NORTH", "SOUTH", "EAST", "WEST"):
        return facing
    else:
        print("The robot can only face NORTH, SOUTH, EAST, or WEST.")
        sys.exit(1)


class Robot:
    @staticmethod
    def place(placement, db_path=DB_PATH):
        """Place the robot on the board."""
        try:
            x, y, facing = placement.split(",")
        except:
            print("Error: invalid placement. Try 'robot --help' for help.")
            sys.exit(1)
        x = validate_coordinate(x)
        y = validate_coordinate(y)
        facing = validate_facing(facing)
        with robot_db(db_path) as db:
            db.upsert(table.Document({"x": x, "y": y, "facing": facing}, doc_id=1))

    @staticmethod
    def report(db_path=DB_PATH):
        """Report the robot's position on the board."""
        with robot_db(db_path) as db:
            robot = db.all()[0]
            x, y, facing = robot["x"], robot["y"], robot["facing"]
            print(f"{x},{y},{facing}")

    @staticmethod
    def move(db_path=DB_PATH):
        """Move the robot one square in the direction it's facing, if possible."""
        with robot_db(db_path) as db:
            robot = db.all()[0]
            if robot["facing"] == "NORTH" and robot["y"] < 4:
                db.update(increment("y"))
            elif robot["facing"] == "SOUTH" and robot["y"] > 0:
                db.update(decrement("y"))
            elif robot["facing"] == "EAST" and robot["x"] < 4:
                db.update(increment("x"))
            elif robot["facing"] == "WEST" and robot["x"] > 0:
                db.update(decrement("x"))
            else:
                print("I'm sorry Dave, I'm afraid I can't do that.")

    @staticmethod
    def rotate(direction, db_path=DB_PATH):
        """Rotate the robot 90 degrees [anti]clockwise."""
        if direction not in ("LEFT", "RIGHT"):
            print("The robot can only rotate LEFT OR RIGHT.")
            sys.exit(1)
        with robot_db(db_path) as db:
            robot = db.all()[0]
            if robot["facing"] == "NORTH":
                facing = "EAST" if direction == "RIGHT" else "WEST"
            elif robot["facing"] == "SOUTH":
                facing = "WEST" if direction == "RIGHT" else "EAST"
            elif robot["facing"] == "EAST":
                facing = "SOUTH" if direction == "RIGHT" else "NORTH"
            elif robot["facing"] == "WEST":
                facing = "NORTH" if direction == "RIGHT" else "SOUTH"
            db.update({"facing": facing})

    def __repr__(self):
        return f"{self.x},{self.y},{self.facing}"
