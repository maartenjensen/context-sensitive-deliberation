# Context sensitive deliberation
import random
from enum import Enum


class ActionType(Enum):  # This will change to being context dependent
    NONE = -1
    DIRECT_AVAILABLE = 0
    FUTURE_AVAILABLE = 1


class Action:

    def __init__(self, effect: str, a_type: ActionType):
        self.effect = effect
        self.a_type = a_type

    def name(self) -> str:
        return type(self).__name__

    def to_str(self) -> str:
        return self.effect + " (" + self.a_type.name + ")"


class Goal(Enum):
    GO_TO_WORK = 0
    DO_NOTHING = 1


class Law(Enum):
    ALLOWED_TO_WORK = 0


class Context:

    def __init__(self):
        self.actions = []
        self.goal = []
        self.beliefs = []
        self.norms = []
        self.laws = []

    def has_goal(self):
        return len(self.goal) > 0

    def has_laws_eval(self):
        return len(self.laws) > 0

    def random_action(self):
        if len(self.actions) > 0:
            return self.actions[random.randint(0, len(self.actions) - 1)]
        else:
            return Criteria.ACTION_FINDING

    def add_actions(self, p_actions: []):
        for action in p_actions:
            add = True
            for existing_action in self.actions:
                if action.effect == existing_action.effect:
                    add = False
                    break
            if add:
                self.actions.append(action)

    def add_goal(self, p_goals: list):
        print(p_goals)
        for goal in p_goals:
            add = True
            for existing_goal in self.goal:
                if goal == existing_goal:
                    add = False
                    break
            if add:
                self.goal.append(goal)

    def add_laws(self, p_laws: list):
        print(p_laws)
        for law in p_laws:
            add = True
            for existing_law in self.laws:
                if law == existing_law:
                    add = False
                    break
            if add:
                self.laws.append(law)

    def clear(self):
        self.actions = []
        self.goal = []
        self.beliefs = []
        self.norms = []
        self.laws = []

    def print_context(self):
        for i in self.actions:
            print(i.to_str())

        for i in self.goal:
            print(i)


class ContextModule:

    # In all the get functions of the ContextModule, the ContextModule should do this from the perspective of the agent
    def __init__(self):
        print("Initialized:" + type(self).__name__)

        self.actions = []
        self.init_actions()

    def init_actions(self):
        self.actions.append(Action("Nothing", ActionType.DIRECT_AVAILABLE))
        self.actions.append(Action("Drink coffee", ActionType.DIRECT_AVAILABLE))
        self.actions.append(Action("Travel to work", ActionType.DIRECT_AVAILABLE))
        self.actions.append(Action("Travel with bike", ActionType.DIRECT_AVAILABLE))
        self.actions.append(Action("Work", ActionType.FUTURE_AVAILABLE))

    def get_actions(self, a_type: ActionType):
        r_actions = []
        for action in self.actions:
            if action.a_type == a_type or a_type == ActionType.NONE:
                r_actions.append(action)
        return r_actions

    def get_goal_context(self):
        return Goal.GO_TO_WORK

    def get_goal_imitation(self):
        return Goal.DO_NOTHING


class Criteria(Enum):
    # Logics criteria
    ERROR = -1
    ACTION_FINDING = 0
    FIND_GOAL = 1
    LAW_EVALUATION = 2

    # Need based criteria
    CONFORMITY = 3
