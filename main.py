"""
    GIT: https://www.youtube.com/watch?v=-_g3QITLaQA&t=173s
    https://stackoverflow.com/questions/18529206/when-do-i-need-to-do-git-pull-before-or-after-git-add-git-commit
    https://pythonprogramming.altervista.org/nice-gui-graphic-for-tkinter-with-ttk-and-azure-theme-from-this-guy/
"""
# Imports
import tkinter as tk
# import random
# random.seed(10)
from Agent import *

window = tk.Tk()
greeting = tk.Label(text="Hello Maarten /Tkinter")
greeting.pack()

myAgent = Agent()
myAgent.deliberate()

window.mainloop()
