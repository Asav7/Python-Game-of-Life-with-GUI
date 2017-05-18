import random
import numpy as np
import tkinter as tk


def get_neighbors(row_index, col_index, array):
    """
    :return: integer: number of neighbours for cell located in the array at (row_index, col_index)
    """
    return np.sum(array[row_index - 1: row_index + 2, col_index - 1: col_index + 2]) - array[row_index, col_index]


def create_tag(row_index, col_index):
    """
    creates tag for identifying cells drawn on canvas.
    :return: string: "row_index-col_index"
    """
    return str(row_index) + "-" + str(col_index)


class Grid(object):

    def __init__(self, width, height, master):
        """
        :param width: grid's width (in cells)
        :param height: grid's width (in cells)
        """
        self.master = master
        self.width = width
        self.height = height
        self.empty_array = np.array([[0 for x in range(self.width)] for y in range(self.height)])
        self.array = self.empty_array.copy()
        self._cell_width = 10
        self._cell_height = 10
        self._animation_stopped = True
        self.init_app()

    def set_random_state(self, fill_rate=0.25):
        self.clear_window()
        for row_index in range(0, self.height):
            for col_index in range(0, self.width):
                if random.random() <= fill_rate:
                    self.array[row_index, col_index] = 1
                else:
                    self.array[row_index, col_index] = 0
        self.visualize_array()

    def step_and_draw(self):
        array_post_step = self.array.copy()
        for row_index in range(self.height):
            for col_index in range(self.width):
                if self.array[row_index, col_index] == 0:  # cell is dead
                    if get_neighbors(row_index, col_index, self.array) == 3:
                        array_post_step[row_index, col_index] = 1
                        self.canvas.create_rectangle(
                            col_index * self._cell_width,
                            row_index * self._cell_height,
                            col_index * self._cell_width + self._cell_width,
                            row_index * self._cell_height + self._cell_height,
                            fill="#550000",
                            tags=(create_tag(row_index, col_index)),
                        )
                else:  # cell is alive
                    if get_neighbors(row_index, col_index, self.array) not in (2, 3):
                        array_post_step[row_index, col_index] = 0
                        self.canvas.delete(self.canvas.find_withtag(create_tag(row_index, col_index)))
        self.array = array_post_step

    def visualize_array(self):

        for row_index in range(self.height):
            for col_index in range(self.width):
                if self.array[row_index, col_index] == 1:
                    self.canvas.create_rectangle(
                        col_index * self._cell_width,
                        row_index * self._cell_height,
                        col_index * self._cell_width + self._cell_width,
                        row_index * self._cell_height + self._cell_height,
                        fill="#550000",
                        tags=(create_tag(row_index, col_index)),
                    )

    def animate(self):
        if self._animation_stopped is False:
            self.step_and_draw()
            self.master.after(1, self.animate)

    def begin_animation(self, *args):
        if self._animation_stopped is True:
            self._animation_stopped = False
            self.master.after(0, self.animate)

    def stop_animation(self, *args):
        self._animation_stopped = True

    def take_one_step(self, *args):
        self.step_and_draw()
        self.stop_animation()

    def clear_window(self, *args):
        self.stop_animation()
        self.array = self.empty_array.copy()
        self.canvas.delete(tk.ALL)

    def gosper_glider_gun(self, *args):
        self.clear_window()
        coordinates = [
            (6, 1), (5, 1), (5, 2), (6, 2), (5, 11), (6, 11), (7, 11), (8, 12), (9, 13), (9, 14), (8, 16), (7, 17),
            (6, 17), (5, 17), (4, 16), (3, 14), (3, 13), (4, 12), (6, 15), (6, 18), (5, 21), (4, 21), (3, 21), (5, 22),
            (4, 22), (3, 22), (2, 23), (6, 23), (2, 25), (6, 25), (1, 25), (7, 25), (3, 35), (4, 35), (3, 36), (4, 36),
            ]
        for coordinates_tuple in coordinates:
            self.array[coordinates_tuple[0], coordinates_tuple[1]] = 1
        self.visualize_array()

    def init_app(self):
        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0, sticky=tk.W)

        tk.Label(frame, text="Fill rate:").grid(row=0, column=0, sticky=tk.W, padx=4)

        fill_rate_entry = tk.Entry(frame)
        fill_rate_entry.grid(row=0, column=1, sticky=tk.W, padx=4)
        fill_rate_entry.insert(0, 0.25)

        set_random_button = tk.Button(frame, text="Set random state")
        set_random_button.bind("<Button-1>", lambda x: self.set_random_state(fill_rate=float(fill_rate_entry.get())))
        set_random_button.grid(row=0, column=2, sticky=tk.W)

        clear_window = tk.Button(frame, text="Clear window")
        clear_window.bind("<Button-1>", self.clear_window)
        clear_window.grid(row=0, column=3, sticky=tk.W)

        run_animation = tk.Button(frame, text="Run animation")
        run_animation.bind("<Button-1>", self.begin_animation)
        run_animation.grid(row=0, column=4)

        stop_animation_button = tk.Button(frame, text="Stop animation")
        stop_animation_button.bind("<Button-1>", self.stop_animation)
        stop_animation_button.grid(row=0, column=5)

        take_one_step = tk.Button(frame, text="Take one step")
        take_one_step.bind("<Button-1>", self.take_one_step)
        take_one_step.grid(row=0, column=6)

        gosper_glider_gun = tk.Button(frame, text="Gosper Glider Gun")
        gosper_glider_gun.bind("<Button-1>", self.gosper_glider_gun)
        gosper_glider_gun.grid(row=0, column=7)

        self.canvas = tk.Canvas(
            self.master,
            width=self.width * self._cell_width,
            height=self.height * self._cell_height,
            relief=tk.GROOVE,
            bd=2,
            )
        self.canvas.grid(row=1, column=0, padx=5, pady=5)

        self.set_random_state()


def main():
    root = tk.Tk()
    root.title("Conway's Game of Life")
    Grid(width=80, height=55, master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
