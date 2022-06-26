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

# myAgent = Agent()
# myAgent.deliberate()

# window.mainloop()

class ContextEnum(Enum):
    ACTIONS = 0
    GOALS = 1
    ACCESSIBLE_OBJECTS = 2


# Basis class for storing parts of the context
class ContextElement:

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


# Keep it simple, for now its only location and affordances
class Locations(Enum):
    BEDROOM = 0
    HOME = 1
    OUTSIDE = 2
    OFFICE = 3


class CE_affordances(ContextElement):

    def __init__(self):
        super().__init__()


class CE_location(ContextElement):

    def __init__(self):
        super().__init__()


class CE_actions_others(ContextElement):

    def __init__(self):
        super().__init__()


class Context:

    def __init__(self):
        self.afford = CE_affordances()
        self.location = CE_location()
        self.actions = CE_actions_others()

    def print_context(self):
        print("PRINT current context")
        print("- Afford: " + str(self.afford.get_data()))
        print("- Location: " + str(self.location.get_data()))
        print("- Actions others: " + str(self.actions.get_data()))


# Example context
myContext = Context()
myContext.afford.add_data([Afford.CAR])
myContext.afford.add_data([Afford.DESK])
myContext.afford.add_data([Afford.DESK])

myContext.print_context()


#
class DeliberationFocus(Enum):
    CONTEXT_EXPANSION = 0
    ACTION_FINDING = 1


class ContextComponent:

    def __init__(self, computational_effort: int, criteria_list: list):
        self.cog_eff = computational_effort
        self.criteria_list = criteria_list  # Change this to a list of objects/enums??

    def explore_context(self, p_context: Context):
        print("Expand context")
        return Criteria.ERROR, False  # Return Criteria OR action and return whether it has to be removed

    def check_criteria(self, new_criteria_list):
        for new_criteria in new_criteria_list:
            if new_criteria not in self.criteria_list:
                return False
        return True

    def name(self) -> str:
        return type(self).__name__


class CC_minimal(ContextComponent):

    def __init__(self):
        super().__init__(1, [])

    def explore_context(self, p_context: Context):
        print("Expand minimal context")
        return DeliberationFocus.ACTION_FINDING, False


class CC_repetition(ContextComponent):

    def __init__(self):
        super().__init__(1, [])

    def explore_context(self, p_context: Context):
        print("Expand context")
        return Criteria.ERROR, False


all_cc = [ContextComponent(0, ['Test'])]  # This is a sorted list based on computational_effort
all_cc.pop()
all_cc.append(DC_default_action())
all_cc.append(DC_goal_from_context())
all_cc.append(DC_goal_from_imitation())
all_cc.append(DC_plan_making())
all_cc.append(DC_end())

in_cc = all_cc
current_cc = None
out_cc = []
