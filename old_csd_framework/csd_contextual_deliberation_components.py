from old_csd_framework.csd_context import *

class DeliberationComponent:
    def __init__(self, computational_effort: int, criteria_list: list):
        self.cog_eff = computational_effort
        self.criteria_list = criteria_list  # Change this to a list of objects/enums??

    def deliberate(self, p_context: CurrentContext) -> tuple[[], bool]:
        print("Deliberate")
        return [DelibFocus.ERROR], False  # Return DelibFocus OR action and return whether it has to be removed

    def check_criteria(self, new_criteria_list):
        for new_criteria in new_criteria_list:
            if new_criteria not in self.criteria_list:
                return False
        return True

    def name(self) -> str:
        return type(self).__name__

class DC_default_action(DeliberationComponent):

    def __init__(self):
        super().__init__(1, [DelibFocus.ACTION_FINDING])

    def deliberate(self, p_context: CurrentContext) -> tuple[[], bool]:
        # This code should check if there is a default action available for this activity in this context
        # Only directly available actions (Sometimes available)
        t_action = Action.NONE
        t_location = p_context.location.get_first_data()
        t_activity = p_context.activity.get_first_data()

        if t_action != Action.NONE:
            print("Found default action:" + str(type(t_action).__name__))
            return [t_action], True
        else:
            print("No default action available")
            return [DelibFocus.ACTION_FINDING], True


class DC_end(DeliberationComponent):

    def __init__(self):
        super().__init__(1000, [DelibFocus.ACTION_FINDING, DelibFocus.FIND_GOAL])

    def deliberate(self, p_context: CurrentContext) -> tuple[[], bool]:
        print("ERROR: DC_end should not have been used")
        return [Action.NONE], False


"""
class DC_plan_making(DeliberationComponent):

    def __init__(self):
        super().__init__(10, [DelibFocus.ACTION_FINDING])

    def deliberate(self, p_context: ContextModule):
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

    def deliberate(self, p_context: ContextModule):
        if random.random() < 0.4:
            print("Added law from imitation:" + str(Goal.DO_NOTHING))
            p_context.add_law([Goal.DO_NOTHING])
            return DelibFocus.ACTION_FINDING, True
        else:
            print("Didn't find law evaluation from imitation")
            return DelibFocus.FIND_GOAL, True

"""
