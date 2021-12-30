from scripts.robot_model import Robot
from scripts.interface import Menu
from scripts.labyrinth import Labyrinth
from scripts.constants import DRAW_PRESCALER, LABYRINTH_WALL_SIZE, TOTAL_SIZE, LABYRINTH_SIZE
import easygraphics as graphics


def draw_robot(robot: Robot):
    last_color = graphics.get_fill_color()
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
    graphics.set_fill_color(last_color)


def draw_map(labyrinth: Labyrinth, color=graphics.Color.GREEN):
    last_fill_color = graphics.get_fill_color()
    graphics.set_fill_color(color)
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
    graphics.set_fill_color(last_fill_color)


def draw_mess_editor():
    last_color = graphics.get_color()
    graphics.set_color(0xFFFFFF)
    graphics.draw_text(TOTAL_SIZE * DRAW_PRESCALER + 100, 300, "Press:")
    graphics.draw_text(TOTAL_SIZE * DRAW_PRESCALER + 120, 330, "x to go back to menu")
    graphics.draw_text(TOTAL_SIZE * DRAW_PRESCALER + 120, 360, "s to save map")


def draw_mess_sim():
    last_color = graphics.get_color()
    graphics.set_color(0xFFFFFF)
    graphics.draw_text(TOTAL_SIZE * DRAW_PRESCALER + 100, 300, "Press:")
    graphics.draw_text(TOTAL_SIZE * DRAW_PRESCALER + 120, 330, "x to go back to menu")
    graphics.draw_text(TOTAL_SIZE * DRAW_PRESCALER + 120, 360, "l to load map")


def draw_menu(menu: Menu):
    text_offset_y = menu.size.y / 2 + 5
    text_offset_x = 20
    last_fill_color = graphics.get_fill_color()
    last_draw_color = graphics.get_color()
    graphics.set_color(graphics.Color.BLACK)
    darker_cyan = 0x00E0E0
    graphics.set_fill_color(darker_cyan)
    x, y = graphics.get_cursor_pos()
    for i in range(len(menu.options)):
        if menu.offset.x < x < (menu.offset.x + menu.size.x) and (
                menu.offset.y + menu.gap * i + menu.size.y * i) < y < (
                menu.offset.y + menu.size.y * (i + 1) + menu.gap * i):
            graphics.set_fill_color(graphics.Color.CYAN)
        else:
            graphics.set_fill_color(darker_cyan)
        graphics.fill_rect(menu.offset.x, menu.offset.y + menu.gap * i + menu.size.y * i, menu.offset.x + menu.size.x,
                           menu.offset.y
                           + menu.size.y * (i + 1) + menu.gap * i)
        graphics.draw_text(text_offset_x + menu.offset.x,
                           menu.offset.y + menu.gap * i + text_offset_y + menu.size.y * i,
                           menu.options[i])
    graphics.set_fill_color(last_fill_color)
    graphics.set_color(last_draw_color)
