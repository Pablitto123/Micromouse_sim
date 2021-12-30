from scripts.constants import DRAW_PRESCALER, LABYRINTH_WALL_SIZE, TOTAL_SIZE, LABYRINTH_SIZE
from typing import List, Union, Tuple
import easygraphics as graphics
import math


class Point2D:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        p = Point2D(x, y)
        return p


class DistanceSensor:
    rel_loc: Point2D  # relative to center of robot
    fi: Union[int, float]  # angle in base robot position, 0 deg is horizontal upward
    size: List[float]  # width and length of sensor

    def __init__(self, rel_loc: Point2D, fi: Union[int, float], size: List[float]):
        self.rel_loc = rel_loc
        self.fi = fi
        if len(size) != 2:
            raise ValueError("size must have length of 2")
        self.size = size[:]


class Engine:
    inertia: float = 3
    omega: float = 0
    max_omega_5v: float
    pass


class Frame:
    points: List[Point2D]

    def __init__(self):
        p1 = Point2D(-3, -3)
        p2 = Point2D(-3, 3)
        p3 = Point2D(3, 3)
        p4 = Point2D(3, -3)
        self.points = [p1, p2, p3, p4]


class Robot:
    frame: Frame
    mass: float
    omega: float
    rotation: float
    location: Point2D
    sensors: List[DistanceSensor]
    engines: List[Engine]

    def __init__(self):
        e1 = Engine()
        e2 = Engine()
        self.engines = [e1, e2]
        self.location = Point2D(LABYRINTH_WALL_SIZE / 2, LABYRINTH_WALL_SIZE / 2)
        self.rotation = 40
        self.frame = Frame()
        d1 = DistanceSensor(Point2D(-1 - 2 ** (1 / 2), -3 + 1 + (2 ** 1 / 2)), fi=-90, size=[0.5, 2])
        d2 = DistanceSensor(Point2D(-1 - (2 ** (1 / 2)) / 2, -3 + (2 ** 1 / 2) / 2), fi=-45, size=[0.5, 2])
        d3 = DistanceSensor(Point2D(0, -3), fi=0, size=[0.5, 2])
        d4 = DistanceSensor(Point2D(1 + (2 ** (1 / 2)) / 2, -3 + (2 ** 1 / 2) / 2), fi=45, size=[0.5, 2])
        d5 = DistanceSensor(Point2D(1 + 2 ** (1 / 2), -3 + 1 + (2 ** 1 / 2)), fi=90, size=[0.5, 2])
        self.sensors = [d1, d2, d3, d4, d5]

    def set_engine_voltage(self):
        pass

    def get_sensor_reading(self, sensor: DistanceSensor):
        pass

    def rotate(self,fi):
        self.rotation+=fi
