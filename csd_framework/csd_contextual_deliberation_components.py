from csd_framework.csd_context import *

myContextModule = ContextModule()
actions = myContextModule.get_actions(ActionType.NONE)

""" The main contextual deliberation component classes """
class ContextualDeliberationComponent:
    def __init__(self, computational_effort: int, criteria_list: list):
        self.cog_eff = computational_effort
        self.criteria_list = criteria_list  # Change this to a list of objects/enums??

    def check_criteria(self, new_criteria_list):
        for new_criteria in new_criteria_list:
            if new_criteria not in self.criteria_list:
                return False
        return True

    def name(self) -> str:
        return type(self).__name__


class ContextualComponent(ContextualDeliberationComponent):
    def __init__(self, computational_effort: int, criteria_list: list):
        super().__init__(computational_effort, criteria_list)

    def explore_context(self, p_context: Context):
        print("Expand context")
        return DelibFocus.ERROR, False  # Return DelibFocus OR action and return whether it has to be removed


class DeliberationComponent(ContextualDeliberationComponent):

    def __init__(self, computational_effort: int, criteria_list: list):
        super().__init__(computational_effort, criteria_list)

    def deliberate(self, p_context: Context):
        print("Deliberate")
        return DelibFocus.ERROR, False  # Return DelibFocus OR action and return whether it has to be removed

class DelibFocus(Enum):
    # Logics criteria
    ERROR = -1
    CONTEXT_EXPANSION = 0
    ACTION_FINDING = 1
    FIND_GOAL = 2
    LAW_EVALUATION = 3

    # Need based criteria
    CONFORMITY = 4


""" Contextual component implementations """
class CC_minimal_old(ContextualComponent):

    def __init__(self):
        super().__init__(1, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: Context):
        print("Expand minimal context")
        return DelibFocus.ACTION_FINDING, False


class CC_repetition(ContextualComponent):

    def __init__(self):
        super().__init__(1, [DelibFocus.CONTEXT_EXPANSION])

    def explore_context(self, p_context: Context):
        print("Expand context")
        return DelibFocus.ERROR, False


""" Deliberation component implementations """


class DC_default_action(DeliberationComponent):

    def __init__(self):
        super().__init__(1, [DelibFocus.ACTION_FINDING])

    def deliberate(self, p_context: Context):
        # What this code should actually do is check the minimal context and decide an action
        # Only directly available actions (Sometimes available)
        t_actions = []
        if random.random() < 0.5:
            t_actions = myContextModule.get_actions(ActionType.DIRECT_AVAILABLE)

        if len(t_actions) == 0:
            print("No default action available")
            return DelibFocus.ACTION_FINDING, True
        else:
            t_action = t_actions[random.randint(0, len(t_actions) - 1)]
            print("Found default action:" + str(type(t_action).__name__))
            return t_action, True


class DC_goal_from_context(DeliberationComponent):

    def __init__(self):
        super().__init__(2, [DelibFocus.FIND_GOAL, DelibFocus.CONFORMITY])

    def deliberate(self, p_context: Context):
        if random.random() < 1:
            print("Added goal from context:" + str(Goal.GO_TO_WORK))
            p_context.add_goal([Goal.GO_TO_WORK])  # myContextModule.get_goal_context(Agent)
            return DelibFocus.ACTION_FINDING, True
        else:
            print("Didn't find a goal from context")
            return DelibFocus.FIND_GOAL, True


class DC_goal_from_imitation(DeliberationComponent):

    def __init__(self):
        super().__init__(2, [DelibFocus.FIND_GOAL, DelibFocus.CONFORMITY])

    def deliberate(self, p_context: Context):
        if random.random() < 0.4:
            print("Added goal from imitation:" + str(Goal.DO_NOTHING))
            p_context.add_goal([Goal.DO_NOTHING])
            return DelibFocus.ACTION_FINDING, True
        else:
            print("Didn't find a goal from imitation")
            return DelibFocus.FIND_GOAL, True


class DC_plan_making(DeliberationComponent):

    def __init__(self):
        super().__init__(10, [DelibFocus.ACTION_FINDING])

    def deliberate(self, p_context: Context):
        if not p_context.has_goal():
            print("No goal available")
            return DelibFocus.FIND_GOAL, False

        if not p_context.has_laws_eval() and random.random() < 0.9:
            print("Action forbidden by law")
            return DelibFocus.LAW_EVALUATION, False

        # Add actions
        p_context.add_actions(myContextModule.get_actions(ActionType.DIRECT_AVAILABLE))
        p_context.add_actions(myContextModule.get_actions(ActionType.FUTURE_AVAILABLE))

        # Planning
        act_or_crit = p_context.random_action()
        # Add plan to the context
        return act_or_crit, True


class DC_law_evaluation_imitation(DeliberationComponent):

    def __init__(self):
        super().__init__(1000, [DelibFocus.LAW_EVALUATION])

    def deliberate(self, p_context: Context):
        if random.random() < 0.4:
            print("Added law from imitation:" + str(Goal.DO_NOTHING))
            p_context.add_law([Goal.DO_NOTHING])
            return DelibFocus.ACTION_FINDING, True
        else:
            print("Didn't find law evaluation from imitation")
            return DelibFocus.FIND_GOAL, True


class DC_end(DeliberationComponent):

    def __init__(self):
        super().__init__(1000, [DelibFocus.ACTION_FINDING, DelibFocus.FIND_GOAL])

    def deliberate(self, p_context: Context):
        print("ERROR: DC_end should not have been used")
        return Action("ERROR", ActionType.DIRECT_AVAILABLE), False
