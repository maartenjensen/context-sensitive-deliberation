# Context sensitive deliberation
import random
from enum import Enum

class DelibFocus(Enum):
    # Logics criteria
    ERROR = -1
    CONTEXT_EXPANSION = 0
    ACTION_FINDING = 1
    FIND_GOAL = 2
    LAW_EVALUATION = 3

    # Need based criteria
    CONFORMITY = 4


class ContextExplorationExclusion(Enum):
    NO_DIRECT_PEOPLE = 0
    NO_DIRECT_GROUPS = 1


class Activity(Enum):
    NONE = -1
    MORNING_ROUTINE = 0
    WORK = 1
    SHOPPING_FOOD = 2
    RELAXING = 3


class Action(Enum):
    NONE = -1
    GET_OUT_OF_BED = 0
    TURN_OF_ALARM = 1
    TAKE_A_SHOWER = 2
    EAT = 3
    DRIVE_TO_LOCATION = 4
    BIKE_TO_LOCATION = 5
    WORK = 6
    BUY_FOOD = 7


class Goal(Enum):
    GET_TO_WORK = 0
    PERFORM_MORNING_ROUTINE = 1
    GET_FOOD = 2
    BE_A_GOOD_EMPLOYEE = 3


# Keep it simple, for now its only location (not time) and affordances
class Location(Enum):
    BEDROOM = 0
    HOME = 1
    OUTSIDE = 2
    OFFICE = 3
    SHOP = 4


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

    PERSON_SHOP_ATTENDANT = 8


"""####################################
           Context element
####################################"""


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

    def get_first_data(self):
        try:
            return self.data[0]
        except ValueError:
            print('self.data does not contain any values')

    def check_data(self, a_data):
        return a_data in self.data

    def has_data(self):
        return len(self.data) > 0


class CE_affordances(ContextElement):
    def __init__(self): super().__init__()


class CE_location(ContextElement):
    def __init__(self): super().__init__()


class CE_actions_others(ContextElement):
    def __init__(self): super().__init__()


class CE_goals_others(ContextElement):
    def __init__(self): super().__init__()


class CE_activity(ContextElement):
    def __init__(self): super().__init__()


class CE_goal(ContextElement):
    def __init__(self): super().__init__()


class Context_exploration_exclusion(ContextElement):
    def __init__(self): super().__init__()


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


"""####################################
           Context class
####################################"""

class CurrentContext:

    def __init__(self):
        self.main_focus = Main_focus()
        self.context_exploration_exclusion = Context_exploration_exclusion()
        self.location = CE_location()
        self.activity = CE_activity()
        self.afford = CE_affordances()
        self.goal = CE_goal()
        self.actions_others = CE_actions_others()
        self.goals_others = CE_goals_others()

    def print_context(self):
        print("- PRINT current context")
        print("- Main focus: " + str(self.main_focus.get_focus()))
        print("- Exploration exclusion: " + str(self.context_exploration_exclusion.get_data()))
        print("- Location: " + str(self.location.get_data()))
        print("- Activity: " + str(self.activity.get_data()))
        print("- Afford: " + str(self.afford.get_data()))
        print("- Goal: " + str(self.goal.get_data()))
        print("- Actions others: " + str(self.actions_others.get_data()))
        print("- Goals others: " + str(self.goals_others.get_data()))

    def print_relevant_context(self):
        print("- PRINT current context")
        if self.main_focus.has_focus():
            print("- Main focus: " + str(self.main_focus.get_focus()))
        if self.context_exploration_exclusion.has_data():
            print("- Exploration exclusion: " + str(self.context_exploration_exclusion.get_data()))
        if self.location.has_data():
            print("- Location: " + str(self.location.get_data()))
        if self.activity.has_data():
            print("- Activity: " + str(self.activity.get_data()))
        if self.afford.has_data():
            print("- Afford: " + str(self.afford.get_data()))
        if self.goal.has_data():
            print("- Goal: " + str(self.goal.get_data()))
        if self.actions_others.has_data():
            print("- Actions others: " + str(self.actions_others.get_data()))
        if self.goals_others.has_data():
            print("- Goals others: " + str(self.goals_others.get_data()))

    def clear(self):
        self.main_focus = Main_focus()
        self.context_exploration_exclusion = Context_exploration_exclusion()
        self.location = CE_location()
        self.activity = CE_activity()
        self.afford = CE_affordances()
        self.goal = CE_goal()
        self.actions_others = CE_actions_others()
        self.goals_others = CE_goals_others()

"""####################################
      Context Expansion Functions
####################################"""

class ContextExpansionFunction:
    def __init__(self, computational_effort: int, criteria_list: list):
        self.cog_eff = computational_effort
        self.criteria_list = criteria_list  # Change this to a list of objects/enums??

    def explore_context(self, p_context: CurrentContext) -> tuple[[], bool]:
        print("Context:" + str(p_context.print_context()))
        print(self.cog_eff)
        return [DelibFocus.ERROR], False

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

    def explore_context(self, p_context: CurrentContext, p_main_focus=Activity.MORNING_ROUTINE,
                        p_location=Location.BEDROOM) -> tuple[[], bool]:  # These last parameters should be removed
        main_focus = p_main_focus  # Get his information from the agent
        p_context.main_focus.set_main_focus(main_focus)
        p_context.activity.add_data([main_focus])
        p_context.location.add_data([p_location])
        return [DelibFocus.ACTION_FINDING], True


class CC_affordances(ContextExpansionFunction):

    def __init__(self):
        super().__init__(1, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: CurrentContext) -> tuple[[], bool]:
        main_focus = p_context.main_focus.get_focus()
        if main_focus == Activity.NONE:
            print("Error")
        elif main_focus == Activity.MORNING_ROUTINE:
            p_context.afford.add_data([Afford.BED, Afford.ALARM_CLOCK, Afford.SHOWER, Afford.BIKE])
        elif main_focus == Activity.WORK:
            p_context.afford.add_data([Afford.CHAIR, Afford.DESK, Afford.COMPUTER])

        return [DelibFocus.ACTION_FINDING], True


class CC_affordances_people(ContextExpansionFunction):

    def __init__(self):
        super().__init__(1, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: CurrentContext) -> tuple[[], bool]:
        main_focus = p_context.main_focus.get_focus()
        location = p_context.location.get_data()[0]
        if location == Location.SHOP:
            p_context.afford.add_data([Afford.PERSON_SHOP_ATTENDANT])
        elif location == Location.BEDROOM:
            p_context.context_exploration_exclusion.add_data([ContextExplorationExclusion.NO_DIRECT_PEOPLE])

        return [DelibFocus.ACTION_FINDING], True


class CC_imitate_action(ContextExpansionFunction):

    def __init__(self):
        super().__init__(5, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: CurrentContext) -> tuple[[], bool]:
        location = p_context.location.get_data()[0]
        if location == Location.SHOP:
            p_context.actions_others.add_data([Action.BUY_FOOD])
        elif location == Location.OFFICE:
            p_context.actions_others.add_data([Action.WORK])
        else:
            return [DelibFocus.CONTEXT_EXPANSION], True

        return [DelibFocus.ACTION_FINDING], True


class CC_imitate_goal(ContextExpansionFunction):

    def __init__(self):
        super().__init__(5, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: CurrentContext) -> tuple[[], bool]:
        location = p_context.location.get_data()[0]
        if location == Location.SHOP:
            p_context.goals_others.add_data([Goal.GET_FOOD])
        elif location == Location.OFFICE:
            p_context.goals_others.add_data([Goal.BE_A_GOOD_EMPLOYEE])
        elif location == Location.OUTSIDE:
            p_context.goals_others.add_data([Goal.GET_TO_WORK])
        else:
            return DelibFocus.CONTEXT_EXPANSION, True

        return [DelibFocus.ACTION_FINDING], True


class CC_end(ContextExpansionFunction):

    def __init__(self):
        super().__init__(1000, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: CurrentContext) -> tuple[[], bool]:
        print("ERRRRRRRROOOOOOOORR")
        return [DelibFocus.ACTION_FINDING], True

