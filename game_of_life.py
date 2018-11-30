import numpy as np
import tkinter as tk


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
        self.canvas = None
        # Initialize GUI
        self.init_app()

    @staticmethod
    def get_neighbors(row_index, col_index, array):
        """ Returns integer - number of neighbours for cell located in the array at (row_index, col_index) """
        return np.sum(array[row_index - 1: row_index + 2, col_index - 1: col_index + 2]) - array[
            row_index, col_index]

    @staticmethod
    def create_tag(row_index, col_index):
        """ Creates tag (string) for identifying cell with (row_index, col_index) drawn on canvas. """
        return str(row_index) + "-" + str(col_index)

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
                if self.get_neighbors(row_index, col_index, self.array) == 3:
                    array_post_step[row_index, col_index] = 1
                    self.fill_cell(col_index, row_index)

            # If cell is alive
            else:
                if self.get_neighbors(row_index, col_index, self.array) not in (2, 3):
                    array_post_step[row_index, col_index] = 0
                    self.canvas.delete(self.canvas.find_withtag(self.create_tag(row_index, col_index)))
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
            tags=(self.create_tag(row_index, col_index)),
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

        # Create helper function for creating buttons.
        def create_button(master, text, bind_function, row, column, **kw):
            """
            Helper function for creating buttons
            """
            button = tk.Button(master, text=text)
            button.bind("<Button-1>", bind_function)
            button.grid(row=row, column=column, **kw)

        # Create buttons:
        # for randomly filling specified grid percentage.
        create_button(frame, "Set random state", row=0, column=2, sticky=tk.W,
                      bind_function=lambda x: self.set_random_state(fill_rate=float(fill_rate_entry.get())))
        # for deleting all filled cells
        create_button(frame, "Clear window new", self.clear_window, row=0, column=3, sticky=tk.W)
        # for starting animation from current state
        create_button(frame, "Run animation", self.begin_animation, row=0, column=4)
        # for stopping animation on current state
        create_button(frame, "Stop animation", self.stop_animation, row=0, column=5)
        # for moving into next step of the animation
        create_button(frame, "Take one step", self.take_one_step, row=0, column=6)
        # for creating a new animation with Gosper Glider Gun
        create_button(frame, "Gosper Glider Gun", self.gosper_glider_gun, row=0, column=7)
        # All buttons created

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
