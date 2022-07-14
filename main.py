"""
    GIT: https://www.youtube.com/watch?v=-_g3QITLaQA&t=173s
    https://stackoverflow.com/questions/18529206/when-do-i-need-to-do-git-pull-before-or-after-git-add-git-commit
    https://pythonprogramming.altervista.org/nice-gui-graphic-for-tkinter-with-ttk-and-azure-theme-from-this-guy/
"""
# Imports
# import random, random.seed(10)
import tkinter as tk
import matplotlib as m_plt
import matplotlib.pyplot as plt

from enum import Enum
from Agent import *
from gui_plotting import UpdatingPlot

"""-------------------
    CONTEXT CODE
-------------------"""


myAgent = Agent()
myAgent.deliberate()

class SimulatedWorld:

    def __init__(self, p_context):
        self.theWorld = p_context


# Example context
fullContext = CurrentContext()
fullContext.afford.add_data([Afford.BED, Afford.ALARM_CLOCK, Afford.SHOWER, Afford.BIKE])
fullContext.activity.add_data([Activity.MORNING_ROUTINE])

print("PRINT full context")
fullContext.print_context()

mySimulation = SimulatedWorld(fullContext)

myContext = CurrentContext()
myContext.print_context()
CC_minimal().explore_context()
CC_minimal().explore_context(myContext, Activity.WORK, Location.OFFICE)
CC_minimal().explore_context(myContext, Activity.SHOPPING_FOOD, Location.SHOP)
CC_minimal().explore_context(myContext, Activity.RELAXING, Location.OUTSIDE)
myContext.print_context()
CC_affordances().explore_context(myContext)
myContext.print_context()
CC_affordances_people().explore_context(myContext)
myContext.print_context()
CC_imitate_action().explore_context(myContext)
myContext.print_context()
CC_imitate_goal().explore_context(myContext)
myContext.print_context()

"""-------------------
    TKINTER SETUP
-------------------"""


def sim_step():
    # model.sim_step()
    plot_field.step()


m_plt.use('TkAgg')
window = tk.Tk()
fig, ax = plt.subplots()
plot_field = UpdatingPlot(master=window, figure=fig)
step_button = tk.Button(master=window, text="step", command=sim_step)

# Package tkinter screen
step_button.pack()
plot_field.get_tk_widget().pack()
window.mainloop()

""" RUBBISH
window = tk.Tk()
myLabel1 = tk.Label(text="Hello Maarten /Tkinter")
myLabel3 = tk.Label(text="My next sentence")


def clickExit():
    print("Pressed Exit! Terminated program")
    exit(0)


def clickPrint():
    print(myEntry.get())

photo1 = tk.PhotoImage(file="figures/my_simulation.png")
#
myEntry = tk.Entry(window, width=30)

myButtonExit = tk.Button(window, text="Exit!", command=clickExit)  # , fg="blue", bg="grey")
myButtonPrint = tk.Button(window, text="Print!", command=clickPrint)

#myLabel1.grid(row=0, column=0) #columnspan
myButtonExit.grid(row=0, column=1)

myButtonPrint.grid(row=1, column=0)
myEntry.grid(row=1, column=1)

myLabel3.grid(row=2, column=1)
tk.Label(window, image=photo1, bg="black").grid(row=0, column=0, sticky=tk.E)


# myAgent = Agent()
# myAgent.deliberate()



window.mainloop()
"""
