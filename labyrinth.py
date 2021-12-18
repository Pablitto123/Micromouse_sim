from robot_model import *
from typing import List, cast
import easygraphics as graphics

LABYRINTH_WALL_SIZE = 18
LABYRINTH_SIZE = 5
TOTAL_SIZE = LABYRINTH_SIZE * LABYRINTH_WALL_SIZE  # 288
DRAW_PRESCALER = 8


class Wall:
    exists: bool
    vert_horiz: str
    location: Point2D
    wall_width: float = 2

    def __init__(self, vert_horiz: str = 'h'):
        p = Point2D(0, 0)
        self.location = p
        if vert_horiz != 'h' and vert_horiz != 'v':
            raise ValueError("can be only h or v")
        self.vert_horiz = vert_horiz


class Labyrinth:
    map: List[List[Wall]]

    def __init__(self):
        self.map = []
        for row_idx in range(2*LABYRINTH_SIZE +1 ):
            row = []
            for col_idx in range(LABYRINTH_SIZE + 1):
                row.append(Wall())
            self.map.append(row)

    def read_map(self, map_file: str):
        try:
            file = open(map_file, 'r')
        except IOError:
            print("File not found or path is incorrect")
            return None
        ind = 0
        for i in range(2*LABYRINTH_SIZE + 1):
            line = file.readline()
            for j in range(LABYRINTH_SIZE + 1):
                ind += 1
                if not i % 2:
                    self.map[i][j].vert_horiz = 'h'
                    self.map[i][j].location.y = i / 2 * LABYRINTH_WALL_SIZE
                    self.map[i][j].location.x = LABYRINTH_WALL_SIZE / 2 + j * LABYRINTH_WALL_SIZE
                else:
                    self.map[i][j].vert_horiz = 'v'
                    self.map[i][j].location.y = i / 2 * LABYRINTH_WALL_SIZE
                    self.map[i][j].location.x = j * LABYRINTH_WALL_SIZE
                if line[j] == '0':
                    self.map[i][j].exists = False
                else:
                    self.map[i][j].exists = True
        file.close()

    def print_map(self):
        for walls in self.map:
            for wall in walls:
                print(wall.vert_horiz, end=' ')
            print('')


def draw_map(labyrinth: Labyrinth):
    for walls in labyrinth.map:
        for wall in walls:
            if wall.vert_horiz == 'v' and wall.exists:
                graphics.fill_rect((wall.location.x - wall.wall_width / 2) * DRAW_PRESCALER,
                                   (wall.location.y - LABYRINTH_WALL_SIZE / 2) * DRAW_PRESCALER,
                                   (wall.location.x + wall.wall_width / 2) * DRAW_PRESCALER,
                                   (wall.location.y + LABYRINTH_WALL_SIZE / 2) * DRAW_PRESCALER)

            if wall.vert_horiz == 'h' and wall.exists:
                graphics.fill_rect((wall.location.x - LABYRINTH_WALL_SIZE / 2) * DRAW_PRESCALER,
                                   (wall.location.y - wall.wall_width / 2) * DRAW_PRESCALER,
                                   (wall.location.x + LABYRINTH_WALL_SIZE / 2) * DRAW_PRESCALER,
                                   (wall.location.y + wall.wall_width / 2) * DRAW_PRESCALER)
