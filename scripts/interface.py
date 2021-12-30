from scripts.labyrinth import Labyrinth, MapEditor
from scripts.robot_model import Robot, Point2D
import scripts.draw as draw
import enum
from typing import Tuple, List
import easygraphics as graphics
import easygraphics.dialog as dialog
import math
from scripts.constants import DRAW_PRESCALER, LABYRINTH_WALL_SIZE, TOTAL_SIZE, LABYRINTH_SIZE


class Mode(enum.Enum):
    START = 0
    MENU = 1
    EDITOR = 2
    SIMULATION = 3


class Menu:
    gap = 3
    offset: Point2D
    size: Point2D
    options: List[str]
    modes: List[Mode]

    def __init__(self):
        self.options = ["Edit map", "Start simulation"]
        self.modes = [Mode.EDITOR, Mode.SIMULATION]
        self.size = Point2D(300, 80)
        self.offset = Point2D(800 - self.size.x / 2, 100)


def is_in_range(v: float, rang: List[float]):
    if rang[0] <= v <= rang[1]:
        return True
    else:
        return False


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


class LabRobInterface:
    @staticmethod
    def where_facing_x(robot: Robot, index):
        sensor = robot.sensors[index]
        sensor_tot_fi = robot.rotation + sensor.fi
        from_0_360 = sensor_tot_fi % 360
        if from_0_360 < 180:
            return 1
        else:
            return -1

    def where_facing_y(robot: Robot, index):
        sensor = robot.sensors[index]
        sensor_tot_fi = robot.rotation + sensor.fi
        from_0_360 = sensor_tot_fi % 360
        if 90 < from_0_360 < 270:
            return 1
        else:
            return -1

    def is_facing_to_point(robot: Robot, x, y, index):
        sensor = robot.sensors[index]
        facing_x = LabRobInterface.where_facing_x(robot, index)
        facing_y = LabRobInterface.where_facing_y(robot, index)
        sensor_tot_fi = robot.rotation + sensor.fi
        tot_rel_x = sensor.rel_loc.x * math.cos(math.radians(robot.rotation)) - sensor.rel_loc.y * math.sin(
            math.radians(robot.rotation))
        tot_rel_y = sensor.rel_loc.x * math.sin(math.radians(robot.rotation)) + sensor.rel_loc.y * math.cos(
            math.radians(robot.rotation))
        tot_loc_y = tot_rel_y + robot.location.y
        tot_loc_x = tot_rel_x + robot.location.x
        if (x-tot_loc_x)*facing_x > 0 and (y-tot_loc_y)*facing_y > 0:
            return True
        else:
            return False
    ## I made a monster
    @staticmethod
    def get_sensor_reading(robot: Robot, lab: Labyrinth, index):
        sensor = robot.sensors[index]
        facing_x = LabRobInterface.where_facing_x(robot, index)
        facing_y = LabRobInterface.where_facing_y(robot, index)
        sensor_tot_fi = robot.rotation + sensor.fi
        tot_rel_x = sensor.rel_loc.x * math.cos(math.radians(robot.rotation)) - sensor.rel_loc.y * math.sin(
            math.radians(robot.rotation))
        tot_rel_y = sensor.rel_loc.x * math.sin(math.radians(robot.rotation)) + sensor.rel_loc.y * math.cos(
            math.radians(robot.rotation))

        tot_loc_y = tot_rel_y + robot.location.y
        tot_loc_x = tot_rel_x + robot.location.x
        b = 0
        a = -1 / math.tan(math.radians(sensor_tot_fi))
        if sensor_tot_fi % 180:
            b = tot_loc_y - a * tot_loc_x
        y_f = lambda x: a * x + b
        x_f = lambda y: (y - b) / a
        width = lab.map[0][0].wall_width
        min_distance = math.inf
        y0_0 = math.inf
        y0_1 = math.inf
        x0_0 = math.inf
        x0_1 = math.inf
        min_point = Point2D(0, 0)
        for i in range(len(lab.map)):
            for j in range(len(lab.map[0])):
                loc_x = lab.map[i][j].location.x
                loc_y = lab.map[i][j].location.y
                if lab.map[i][j].exists and lab.map[i][j].vert_horiz == 'h':
                    x_range = [loc_x - LABYRINTH_WALL_SIZE / 2, loc_x + LABYRINTH_WALL_SIZE / 2]
                    y_range = [loc_y - width / 2, width / 2 + loc_y]
                    y0_0 = loc_y - width / 2
                    y0_1 = loc_y + width / 2
                    x0_0 = loc_x - LABYRINTH_WALL_SIZE / 2
                    x0_1 = loc_x + LABYRINTH_WALL_SIZE / 2
                elif lab.map[i][j].exists and lab.map[i][j].vert_horiz == 'v':
                    x_range = [loc_x - width / 2, loc_x + width / 2]
                    y_range = [loc_y - LABYRINTH_WALL_SIZE / 2, loc_y + LABYRINTH_WALL_SIZE / 2]
                    y0_0 = loc_y - LABYRINTH_WALL_SIZE / 2
                    y0_1 = loc_y + LABYRINTH_WALL_SIZE / 2
                    x0_0 = loc_x - width / 2
                    x0_1 = loc_x + width / 2
                else:
                    x_range = [0, 0]
                    y_range = [0, 0]

                if lab.map[i][j].exists:
                    lmd = min_distance
                    if is_in_range(y_f(x0_0), y_range) and is_in_range(x0_0, x_range) and LabRobInterface.is_facing_to_point(robot, x0_0, y_f(x0_0), index):
                        min_distance = min(min_distance, distance(tot_loc_x, tot_loc_y, x0_0, y_f(x0_0)))
                    if min_distance != lmd:
                        min_point.x = x0_0

                    lmd = min_distance
                    if is_in_range(y_f(x0_1), y_range) and is_in_range(x0_1, x_range) and LabRobInterface.is_facing_to_point(robot, x0_1, y_f(x0_1), index):
                        min_distance = min(min_distance, distance(tot_loc_x, tot_loc_y, x0_1, y_f(x0_1)))
                    if min_distance != lmd:
                        min_point.x = x0_1

                    lmd = min_distance
                    if is_in_range(y0_0, y_range) and is_in_range(x_f(y0_0), x_range) and LabRobInterface.is_facing_to_point(robot, x_f(y0_0), y0_0, index):
                        min_distance = min(min_distance, distance(tot_loc_x, tot_loc_y, x_f(y0_0), y0_0))
                    if min_distance != lmd:
                        min_point.x = x_f(y0_0)

                    lmd = min_distance
                    if is_in_range(y0_1, y_range) and is_in_range(x_f(y0_1), x_range) and LabRobInterface.is_facing_to_point(robot, x_f(y0_1), y0_1, index):
                        min_distance = min(min_distance, distance(tot_loc_x, tot_loc_y, x_f(y0_1), y0_1))
                    if min_distance != lmd:
                        min_point.x = x_f(y0_1)

        last_draw_color = graphics.get_color()
        graphics.set_color(graphics.Color.LIGHT_RED)
        min_point.y = y_f(min_point.x)
        graphics.set_line_width(2)
        x_next = (tot_loc_x + 5 * facing_x)
        graphics.fill_circle(tot_loc_x * DRAW_PRESCALER, tot_loc_y * DRAW_PRESCALER, 2)
        graphics.draw_line(tot_loc_x * DRAW_PRESCALER, tot_loc_y * DRAW_PRESCALER, min_point.x * DRAW_PRESCALER,
                           min_point.y * DRAW_PRESCALER)
        graphics.set_color(last_draw_color)
        return min_distance


class Interface:
    lab: Labyrinth
    robot: Robot
    editor: MapEditor
    menu: Menu
    mode: Mode = Mode.START
    end_flag = False

    def __init__(self, lab: Labyrinth, robot: Robot):
        self.lab = lab
        self.robot = robot
        self.menu = Menu()
        self.editor = MapEditor(lab)
        self.img = None

    def begin(self):
        self.img = graphics.create_image_from_file("vriskers-700x451.jpg")
        graphics.init_graph(1600, 900)
        graphics.set_render_mode(graphics.RenderMode.RENDER_MANUAL)
        self.mode = Mode.MENU
        self.loop()
        graphics.close_graph()

    def perform_menu_tasks(self):
        graphics.fill_image(graphics.Color.BLACK)
        x, y = graphics.get_cursor_pos()
        draw.draw_menu(self.menu)
        if graphics.has_mouse_msg():
            msg = graphics.get_mouse_msg()
            if msg.type == graphics.MouseMessageType.PRESS_MESSAGE:
                for i in range(len(self.menu.options)):
                    if self.menu.offset.x < x < (self.menu.offset.x + self.menu.size.x) and (
                            self.menu.offset.y + self.menu.gap * i + self.menu.size.y * i) < y < (
                            self.menu.offset.y + self.menu.size.y * (i + 1) + self.menu.gap * i):
                        self.mode = self.menu.modes[i]

    def perform_editor_tasks(self):
        graphics.fill_image(graphics.Color.BLACK)
        draw.draw_map(self.editor.lab, graphics.Color.DARK_GREEN)
        draw.draw_mess_editor()
        self.editor.edit_map()
        if graphics.has_kb_hit():
            key = graphics.get_char()
            if key == 's':
                name = dialog.get_string("Enter name of file", default_response="map.txt", title="Save map")
                if name is not None:
                    try:
                        self.editor.save_map(name)
                        dialog.show_message("Saved successfully")
                    except:
                        dialog.show_message("failed to save file")

            if key == 'x':
                self.mode = Mode.MENU

    def perform_simulation_tasks(self):
        name = "map.txt"
        graphics.fill_image(graphics.Color.BLACK)
        draw.draw_mess_sim()
        draw.draw_map(self.lab)
        draw.draw_robot(self.robot)
        readings = []
        for i in range(5):
            readings.append(LabRobInterface.get_sensor_reading(self.robot, self.lab, i))
        for i in range(5):
            graphics.draw_text(1000, 200 + i * 20, "czujnik nr.{} : {:.2f}".format(i, readings[i]))
        self.robot.rotate(0.6)

        if graphics.has_kb_hit():
            key = graphics.get_char()
            if key == 'l':
                name = dialog.get_string("Enter name of file", default_response="map.txt", title="Load map")
                if name is not None:
                    self.lab.read_map(name)
            if key == 'x':
                self.mode = Mode.MENU
        pass

    def loop(self):
        while graphics.is_run():
            if graphics.delay_fps(60):
                if self.mode == Mode.MENU:
                    self.perform_menu_tasks()
                elif self.mode == Mode.EDITOR:
                    self.perform_editor_tasks()
                elif self.mode == Mode.SIMULATION:
                    self.perform_simulation_tasks()
