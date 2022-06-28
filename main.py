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

# window = tk.Tk()
# greeting = tk.Label(text="Hello Maarten /Tkinter")
# greeting.pack()

myAgent = Agent()
myAgent.deliberate()


# window.mainloop()

class ContextEnum(Enum):
    ACTIONS = 0
    GOALS = 1
    ACCESSIBLE_OBJECTS = 2


# Basis class for storing parts of the context
class ContextElement:  # ContextExplorationUnit

    def __init__(self):
        self.data = []

    def add_data(self, p_data: []):
        for a_data in p_data:
            if a_data not in self.data:
                self.data.append(a_data)

    def get_data(self) -> []:
        return self.data

    def check_data(self, a_data):
        return a_data in self.data

    def has_data(self):
        return len(self.data) > 0


# This needs to be something else??
# It should be affordances
class Afford(Enum):
    BED = 0
    CHAIR = 1
    ALARM_CLOCK = 2
    BIKE = 3
    CAR = 4
    SHOWER = 5
    DESK = 6
    COMPUTER = 7

class CE_affordances(ContextElement):

    def __init__(self):
        super().__init__()

# Keep it simple, for now its only location and affordances
class Locations(Enum):
    BEDROOM = 0
    HOME = 1
    OUTSIDE = 2
    OFFICE = 3


class CE_location(ContextElement):

    def __init__(self):
        super().__init__()


class CE_actions_others(ContextElement):

    def __init__(self):
        super().__init__()


class Activity(Enum):
    NONE = -1
    MORNING_ROUTINE = 0
    WORK = 1


class CE_activity(ContextElement):

    def __init__(self):
        super().__init__()


class CE_goal(ContextElement):

    def __init__(self):
        super().__init__()


class Main_focus:

    def __init__(self):
        self.main_focus = Activity.NONE

    def set_main_focus(self, p_main_focus: object):
        self.main_focus = p_main_focus

    def check_focus(self, a_data):
        return a_data in self.main_focus

    def get_focus(self):
        return self.main_focus

    def has_focus(self):
        return self.main_focus is not None

class Context:

    def __init__(self):
        self.main_focus = Main_focus()
        self.location = CE_location()
        self.activity = CE_activity()
        self.afford = CE_affordances()
        self.goal = CE_goal()
        self.actions = CE_actions_others()

    def print_context(self):
        print("PRINT current context")
        print("- Main focus: " + str(self.main_focus.get_focus()))
        print("- Location: " + str(self.location.get_data()))
        print("- Activity: " + str(self.activity.get_data()))
        print("- Afford: " + str(self.afford.get_data()))
        print("- Goal: " + str(self.goal.get_data()))
        print("- Actions others: " + str(self.actions.get_data()))


class SimulatedWorld:

    def __init__(self, p_context):
        self.theWorld = p_context


# Example context
fullContext = Context()
fullContext.afford.add_data([Afford.BED, Afford.ALARM_CLOCK, Afford.SHOWER, Afford.BIKE])
fullContext.activity.add_data([Activity.MORNING_ROUTINE])

fullContext.print_context()

mySimulation = SimulatedWorld(fullContext)



class ContextExpansionFunction:
    def __init__(self, computational_effort: int, criteria_list: list):
        self.cog_eff = computational_effort
        self.criteria_list = criteria_list  # Change this to a list of objects/enums??

    def explore_context(self, p_context: Context):
        print("Context:" + str(p_context.print_context()))
        print(self.cog_eff)
        return DelibFocus.ERROR, False

    def check_criteria(self, new_criteria_list):
        for new_criteria in new_criteria_list:
            if new_criteria not in self.criteria_list:
                return False
        return True

    def name(self) -> str:
        return type(self).__name__


class CC_minimal(ContextExpansionFunction):

    def __init__(self):
        super().__init__(1, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: Context):
        main_focus = Activity.MORNING_ROUTINE # Get his information from the agent
        p_context.main_focus.set_main_focus(main_focus)
        p_context.activity.add_data([main_focus])
        p_context.location.add_data([Locations.BEDROOM])
        print(self.cog_eff)
        return DelibFocus.ACTION_FINDING, True


class CC_affordances(ContextExpansionFunction):

    def __init__(self):
        super().__init__(1, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: Context):
        main_focus = p_context.main_focus.get_focus()
        if main_focus == Activity.NONE:
            print("Error")
        elif main_focus == Activity.MORNING_ROUTINE:
            p_context.afford.add_data([Afford.BED, Afford.ALARM_CLOCK, Afford.SHOWER, Afford.BIKE])
        elif main_focus == Activity.WORK:
            p_context.afford.add_data([Afford.CHAIR, Afford.DESK, Afford.COMPUTER])

        return DelibFocus.ACTION_FINDING, True

myContext = Context()
myContext.print_context()
CC_minimal().explore_context(myContext)
myContext.print_context()
CC_affordances().explore_context(myContext)
myContext.print_context()