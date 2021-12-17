from typing import List
from labyrinth import *


class Point2D:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y


class DistanceSensor:

    pass


class Engine:
    pass


class Robot:
    rotation: float
    location: Point2D
    sensors: List[DistanceSensor]
    engines: List[Engine]

    def __init__(self):
        self.location = Point2D(LABYRINTH_WALL_SIZE/2, LABYRINTH_WALL_SIZE/2)
        self.rotation = 0

