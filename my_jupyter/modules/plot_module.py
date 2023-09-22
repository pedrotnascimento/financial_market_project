from matplotlib import pyplot as plt
from IPython.display import display, clear_output
import time


class Plotting:
    plt.ion()
    fig, ax = plt.subplots()
    (line,) = ax.plot([], [])

    def __init__(self):
        pass

    def plot_data(self, x, y):
        self.ax.set_ylim(0, 10)
        self.ax.set_xlim(0, 2 * 60 + 1)
        self.fig.set_figheight(6)
        self.fig.set_figwidth(8)
        y_max = max(y)
        self.ax.set_ylim(0, y_max)
        self.ax.set_xlim(x[0], x[-1])
        self.line.set_data(x, y)

        # Redraw the plot
        display(self.fig)
        clear_output(wait=True)
        time.sleep(2)
