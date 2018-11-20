import numpy as np
import tkinter as tk


def get_neighbors(row_index, col_index, array):
    """
    :return: integer: number of neighbours for cell located in the array at (row_index, col_index)
    """
    return np.sum(array[row_index - 1: row_index + 2, col_index - 1: col_index + 2]) - array[row_index, col_index]


def create_tag(row_index, col_index):
    """
    Creates tag for identifying cell with (row_index, col_index) drawn on canvas.
    :return: String: "row_index-col_index"
    """
    return str(row_index) + "-" + str(col_index)


class Grid(object):

    def __init__(self, width: int, height: int, master: tk.Tk):
        """
        :param width: Integer - how many cells wide should the grid be.
        :param height: Integer - how many cells high should the grid be
        :param master: Tk object instance
        """
        self.master = master
        self.width = width
        self.height = height
        self.array = np.zeros((self.height, self.width))
        self._cell_width = 10
        self._cell_height = 10
        self._animation_stopped = True
        self.init_app()
        self.canvas = None

    def set_random_state(self, fill_rate=0.25):
        """ Marks given percentage (fill_rate) of cells as alive. """
        self.clear_window()
        self.array = (np.random.random(self.array.shape) < fill_rate).astype(int)
        self.visualize_array()

    def step_and_draw(self):
        """ Checks which cells will be alive in the next step and draws the next step of the simulation. """
        array_post_step = self.array.copy()
        for (row_index, col_index), value in np.ndenumerate(array_post_step):

            # If cell is dead:
            if value == 0:
                if get_neighbors(row_index, col_index, self.array) == 3:
                    array_post_step[row_index, col_index] = 1
                    self.fill_cell(col_index, row_index)

            # If cell is alive
            else:
                if get_neighbors(row_index, col_index, self.array) not in (2, 3):
                    array_post_step[row_index, col_index] = 0
                    self.canvas.delete(self.canvas.find_withtag(create_tag(row_index, col_index)))
        self.array = array_post_step  # update array

    def visualize_array(self):
        """ Draws current state of the simulation."""
        for (row_index, col_index), value in np.ndenumerate(self.array):
            if value == 1:
                self.fill_cell(col_index, row_index)

    def fill_cell(self, col_index, row_index, color="#550000"):
        """ Fills one cell located on column index (col_index) and row index (row_index) with given color (color)."""
        self.canvas.create_rectangle(
            col_index * self._cell_width,
            row_index * self._cell_height,
            col_index * self._cell_width + self._cell_width,
            row_index * self._cell_height + self._cell_height,
            fill=color,
            tags=(create_tag(row_index, col_index)),
        )

    def animate(self):
        """ Runs animation """
        if self._animation_stopped is False:
            self.step_and_draw()
            self.master.after(1, self.animate)

    def begin_animation(self, *args):
        """ Starts animation """
        if self._animation_stopped is True:
            self._animation_stopped = False
            self.master.after(0, self.animate)

    def stop_animation(self, *args):
        """ Stops animation """
        self._animation_stopped = True

    def take_one_step(self, *args):
        """ Draws the next step of the simulation """
        self.step_and_draw()
        self.stop_animation()

    def clear_window(self, *args):
        """ Deletes all cells drawn on canvas. """
        self.stop_animation()
        self.array = np.zeros((self.height, self.width))
        self.canvas.delete(tk.ALL)

    def gosper_glider_gun(self, *args):
        """ Draws only the cells which create Gosper Glider Gun in top left corner of the canvas. """
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
        """ Creates GUI """

        # Create frame
        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0, sticky=tk.W)

        # Create entry where user inputs fill rate
        tk.Label(frame, text="Fill rate:").grid(row=0, column=0, sticky=tk.W, padx=4)
        fill_rate_entry = tk.Entry(frame)
        fill_rate_entry.grid(row=0, column=1, sticky=tk.W, padx=4)
        fill_rate_entry.insert(0, 0.25)

        # Create button which will randomly fill specified grid percentage.
        set_random_button = tk.Button(frame, text="Set random state")
        set_random_button.bind("<Button-1>", lambda x: self.set_random_state(fill_rate=float(fill_rate_entry.get())))
        set_random_button.grid(row=0, column=2, sticky=tk.W)

        # Create button for deleting all filled cells
        clear_window = tk.Button(frame, text="Clear window")
        clear_window.bind("<Button-1>", self.clear_window)
        clear_window.grid(row=0, column=3, sticky=tk.W)

        # Create button for starting animation from current state
        run_animation = tk.Button(frame, text="Run animation")
        run_animation.bind("<Button-1>", self.begin_animation)
        run_animation.grid(row=0, column=4)

        # Create button for stopping animation on current state
        stop_animation_button = tk.Button(frame, text="Stop animation")
        stop_animation_button.bind("<Button-1>", self.stop_animation)
        stop_animation_button.grid(row=0, column=5)

        # Create button for moving into next step of the animation
        take_one_step = tk.Button(frame, text="Take one step")
        take_one_step.bind("<Button-1>", self.take_one_step)
        take_one_step.grid(row=0, column=6)

        # Create button which will create new animation with Gosper Glider Gun
        gosper_glider_gun = tk.Button(frame, text="Gosper Glider Gun")
        gosper_glider_gun.bind("<Button-1>", self.gosper_glider_gun)
        gosper_glider_gun.grid(row=0, column=7)

        # Create canvas to draw on
        self.canvas = tk.Canvas(
            self.master,
            width=self.width * self._cell_width,
            height=self.height * self._cell_height,
            relief=tk.GROOVE,
            bd=2,
            )
        self.canvas.grid(row=1, column=0, padx=5, pady=5)

        # Initialize animation with random state
        self.set_random_state()


def main():
    root = tk.Tk()
    root.title("Conway's Game of Life")
    Grid(width=80, height=55, master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
