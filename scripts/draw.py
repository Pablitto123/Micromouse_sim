from scripts.robot_model import Robot
from scripts.labyrinth import Labyrinth
from scripts.constants import DRAW_PRESCALER, LABYRINTH_WALL_SIZE, TOTAL_SIZE, LABYRINTH_SIZE
import easygraphics as graphics

def draw_robot(robot: Robot):
    graphics.set_fill_color(graphics.Color.DARK_RED)
    graphics.rotate(robot.rotation, robot.location.x * DRAW_PRESCALER, robot.location.y * DRAW_PRESCALER)
    left_top_corner = robot.location + robot.frame.points[0]
    right_bottom_corner = robot.location + robot.frame.points[2]
    graphics.fill_rect(left_top_corner.x * DRAW_PRESCALER, left_top_corner.y * DRAW_PRESCALER,
                       right_bottom_corner.x * DRAW_PRESCALER, right_bottom_corner.y * DRAW_PRESCALER)
    graphics.set_fill_color(graphics.Color.DARK_MAGENTA)
    graphics.draw_line(robot.location.x * DRAW_PRESCALER, robot.location.y * DRAW_PRESCALER,
                       robot.location.x * DRAW_PRESCALER,
                       (robot.location.y + robot.frame.points[0].y) * DRAW_PRESCALER)
    graphics.rotate(-robot.rotation, robot.location.x * DRAW_PRESCALER, robot.location.y * DRAW_PRESCALER)
    graphics.set_fill_color(graphics.Color.GREEN)


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
