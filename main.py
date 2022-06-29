"""
    GIT: https://www.youtube.com/watch?v=-_g3QITLaQA&t=173s
    https://stackoverflow.com/questions/18529206/when-do-i-need-to-do-git-pull-before-or-after-git-add-git-commit
    https://pythonprogramming.altervista.org/nice-gui-graphic-for-tkinter-with-ttk-and-azure-theme-from-this-guy/
"""
# Imports
import tkinter as tk
# import random
# random.seed(10)
from enum import Enum
from Agent import *

# window = tk.Tk()
# greeting = tk.Label(text="Hello Maarten /Tkinter")
# greeting.pack()

myAgent = Agent()
myAgent.deliberate()

"""
# window.mainloop()
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
#CC_minimal().explore_context()
#CC_minimal().explore_context(myContext, Activity.WORK, Location.OFFICE)
CC_minimal().explore_context(myContext, Activity.SHOPPING_FOOD, Location.SHOP)
#CC_minimal().explore_context(myContext, Activity.RELAXING, Location.OUTSIDE)
myContext.print_context()
CC_affordances().explore_context(myContext)
myContext.print_context()
CC_affordances_people().explore_context(myContext)
myContext.print_context()
CC_imitate_action().explore_context(myContext)
myContext.print_context()
CC_imitate_goal().explore_context(myContext)
myContext.print_context()
"""