import easygraphics as eg
import labyrinth

laby = labyrinth.Labyrinth()

laby.read_map("map.txt")
laby.print_map()

def mainloop():
    eg.fill_image(color=eg.Color.BLACK)
    eg.set_color(eg.Color.BLUE)
    eg.set_fill_color(eg.Color.GREEN)
    while eg.is_run():
        if eg.delay_jfps(60):
            eg.fill_image(color=eg.Color.BLACK)
            labyrinth.draw_map(laby)


def main():
    eg.init_graph(1800, 1000)
    eg.set_render_mode(eg.RenderMode.RENDER_MANUAL)
    mainloop()
    eg.close_graph()



if __name__ == '__main__':
    eg.easy_run(main)
    pass