import matplotlib as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def install_plot_widgets():
    plt.use("TkAgg")


class UpdatingPlot(FigureCanvasTkAgg):
    def __init__(self, model, plot_function, fargs=(), **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.plot_function = plot_function
        self.fargs = fargs

    def step(self):
        axs = self.figure.axes
        print(axs)
        for ax in axs:
            ax.clear()
        if len(axs) == 1:
            self.plot_function(self.model, axs[0], *self.fargs)
        else:
            self.plot_function(self.model, axs, *self.fargs)
        self.draw()

