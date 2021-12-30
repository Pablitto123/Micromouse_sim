import easygraphics as eg
from scripts import labyrinth
from scripts.robot_model import Robot
from scripts import draw
from scripts.interface import Menu, Interface

menu = Menu()
laby = labyrinth.Labyrinth()
laby.read_map("map.txt")
editor = labyrinth.MapEditor(laby)
editor.lab = laby
robot = Robot()
interface = Interface(laby, robot)


def main():
    interface.begin()


if __name__ == '__main__':
    eg.easy_run(main)
