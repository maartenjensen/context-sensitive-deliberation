"""
PLOTS
"""

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

"""
MODEL
"""

import agentpy as ap

class Person(ap.Agent):

    def setup(self):
        """ Initiate agent attributes. """
        self.grid = self.model.grid
        self.random = self.model.random
        self.group = self.random.choice(range(self.p.n_groups))
        self.share_similar = 0
        self.happy = False

    def update_happiness(self):
        """ Be happy if rate of similar neighbors is high enough. """
        neighbors = self.grid.neighbors(self)
        similar = len([n for n in neighbors if n.group == self.group])
        ln = len(neighbors)
        self.share_similar = similar / ln if ln > 0 else 0
        self.happy = self.share_similar >= self.p.want_similar

    def find_new_home(self):
        """ Move to random free spot and update free spots. """
        new_spot = self.random.choice(self.model.grid.empty)
        self.grid.move_to(self, new_spot)

class SegregationModel(ap.Model):

    def setup(self):

        # Parameters
        s = self.p.size
        n = self.n = int(self.p.density * (s ** 2))

        # Create grid and agents
        self.grid = ap.Grid(self, (s, s), track_empty=True)
        self.agents = ap.AgentList(self, n, Person)
        self.grid.add_agents(self.agents, random=True, empty=True)

    def update(self):
        # Update list of unhappy people
        self.agents.update_happiness()
        self.unhappy = self.agents.select(self.agents.happy == False)

        # Stop simulation if all are happy
        if len(self.unhappy) == 0:
            self.stop()

    def step(self):
        # Move unhappy people to new location
        self.unhappy.find_new_home()

    def get_segregation(self):
        # Calculate average percentage of similar neighbors
        return round(sum(self.agents.share_similar) / self.n, 2)

    def end(self):
        # Measure segregation at the end of the simulation
        self.report('segregation', self.get_segregation())

parameters = {
    'want_similar': 0.3, # For agents to be happy
    'n_groups': 2, # Number of groups
    'density': 0.95, # Density of population
    'size': 50, # Height and length of the grid
    'steps': 50  # Maximum number of steps
    }

def animation_plot(model, ax):
    group_grid = model.grid.attr_grid('group')
    ap.gridplot(group_grid, cmap='Accent', ax=ax)
    ax.set_title(f"Segregation model \n Time-step: {model.t}, "
                 f"Segregation: {model.get_segregation()}")


"""
GUI
"""

import tkinter as tk

model = SegregationModel(parameters)
model.sim_setup()

install_plot_widgets()
root = tk.Tk()
fig, ax = plt.subplots()
plot_field = UpdatingPlot(model, animation_plot, master=root, figure=fig)
def step():
    model.sim_step()
    plot_field.step()
step_button = tk.Button(master=root, text="step", command=step)
step_button.pack()
plot_field.get_tk_widget().pack()
root.mainloop()
