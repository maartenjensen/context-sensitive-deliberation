from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

class UpdatingPlot(FigureCanvasTkAgg):

    def __init__(self, fargs=(), **kwargs):
        super().__init__(**kwargs)
        self.fargs = fargs

    def step(self):
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        y = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])

        plt.scatter(x, y)
        self.draw()