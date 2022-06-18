from csd_framework.csd_context import *

myContextModule = ContextModule()
actions = myContextModule.get_actions(ActionType.NONE)


class DeliberationComponent:

    def __init__(self, computational_effort: int, criteria_list: list):
        self.cog_eff = computational_effort
        self.criteria_list = criteria_list  # Change this to a list of objects/enums??

    def deliberate(self, p_context: Context):
        print("Expand context")
        return Criteria.ERROR, False  # Return Criteria OR action and return whether it has to be removed

    def check_criteria(self, new_criteria_list):
        for new_criteria in new_criteria_list:
            if new_criteria not in self.criteria_list:
                return False
        return True

    def name(self) -> str:
        return type(self).__name__


class DC_default_action(DeliberationComponent):

    def __init__(self):
        super().__init__(1, [Criteria.ACTION_FINDING])

    def deliberate(self, p_context: Context):
        # What this code should actually do is check the minimal context and decide an action
        # Only directly available actions (Sometimes available)
        t_actions = []
        if random.random() < 0.5:
            t_actions = myContextModule.get_actions(ActionType.DIRECT_AVAILABLE)

        if len(t_actions) == 0:
            print("No default action available")
            return Criteria.ACTION_FINDING, True
        else:
            t_action = t_actions[random.randint(0, len(t_actions) - 1)]
            print("Found default action:" + str(type(t_action).__name__))
            return t_action, True


class DC_goal_from_context(DeliberationComponent):

    def __init__(self):
        super().__init__(2, [Criteria.FIND_GOAL, Criteria.CONFORMITY])

    def deliberate(self, p_context: Context):
        if random.random() < 1:
            print("Added goal from context:" + str(Goal.GO_TO_WORK))
            p_context.add_goal([Goal.GO_TO_WORK])  # myContextModule.get_goal_context(Agent)
            return Criteria.ACTION_FINDING, True
        else:
            print("Didn't find a goal from context")
            return Criteria.FIND_GOAL, True


class DC_goal_from_imitation(DeliberationComponent):

    def __init__(self):
        super().__init__(2, [Criteria.FIND_GOAL, Criteria.CONFORMITY])

    def deliberate(self, p_context: Context):
        if random.random() < 0.4:
            print("Added goal from imitation:" + str(Goal.DO_NOTHING))
            p_context.add_goal([Goal.DO_NOTHING])
            return Criteria.ACTION_FINDING, True
        else:
            print("Didn't find a goal from imitation")
            return Criteria.FIND_GOAL, True


class DC_plan_making(DeliberationComponent):

    def __init__(self):
        super().__init__(10, [Criteria.ACTION_FINDING])

    def deliberate(self, p_context: Context):
        if not p_context.has_goal():
            print("No goal available")
            return Criteria.FIND_GOAL, False

        if not p_context.has_laws_eval() and random.random() < 0.9:
            print("Action forbidden by law")
            return Criteria.LAW_EVALUATION, False

        # Add actions
        p_context.add_actions(myContextModule.get_actions(ActionType.DIRECT_AVAILABLE))
        p_context.add_actions(myContextModule.get_actions(ActionType.FUTURE_AVAILABLE))

        # Planning
        act_or_crit = p_context.random_action()
        # Add plan to the context
        return act_or_crit, True


class DC_law_evaluation_imitation(DeliberationComponent):

    def __init__(self):
        super().__init__(1000, [Criteria.LAW_EVALUATION])

    def deliberate(self, p_context: Context):
        if random.random() < 0.4:
            print("Added law from imitation:" + str(Goal.DO_NOTHING))
            p_context.add_law([Goal.DO_NOTHING])
            return Criteria.ACTION_FINDING, True
        else:
            print("Didn't find law evaluation from imitation")
            return Criteria.FIND_GOAL, True


class DC_end(DeliberationComponent):

    def __init__(self):
        super().__init__(1000, [Criteria.ACTION_FINDING, Criteria.FIND_GOAL])

    def deliberate(self, p_context: Context):
        print("ERROR: DC_end should not have been used")
        return Action("ERROR", ActionType.DIRECT_AVAILABLE), False
