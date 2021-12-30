import easygraphics as eg
from scripts import labyrinth
from scripts.robot_model import Robot
from scripts import draw
laby = labyrinth.Labyrinth()
laby.read_map("new_map.txt")
editor = labyrinth.MapEditor(laby)
editor.lab = laby
robot = Robot()
def mainloop():
    eg.fill_image(color=eg.Color.BLACK)
    eg.set_color(eg.Color.BLUE)
    eg.set_fill_color(eg.Color.GREEN)
    while eg.is_run():
        if eg.delay_jfps(60):
            eg.fill_image(color=eg.Color.BLACK)
            if eg.has_kb_hit():
                key = eg.get_char()
                if key == "s":
                    editor.save_map("new_map.txt")
            draw.draw_map(editor.lab)
            editor.edit_map()
            draw.draw_robot(robot)

def main():
    eg.init_graph(1800, 1000)
    eg.set_render_mode(eg.RenderMode.RENDER_MANUAL)
    mainloop()
    eg.close_graph()



if __name__ == '__main__':
    eg.easy_run(main)
