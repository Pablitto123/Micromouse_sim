from scripts.constants import DRAW_PRESCALER, LABYRINTH_WALL_SIZE, TOTAL_SIZE, LABYRINTH_SIZE
from typing import List


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
    pass


class Engine:
    inertia: float = 3
    omega: float = 0
    max_omega_5v: float
    pass


class Frame:
    points: List[Point2D]

    def __init__(self):
        p1 = Point2D(-3, -3)
        p2 = Point2D(-5, 5)
        p3 = Point2D(3, 3)
        p4 = Point2D(5, -5)
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
        self.rotation = 0
        self.frame = Frame()

    def set_engine_voltage(self):
        pass


