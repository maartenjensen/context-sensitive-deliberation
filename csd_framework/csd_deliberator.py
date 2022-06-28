# My classes
from csd_framework.csd_contextual_deliberation_components import *
from csd_framework.csd_context import *

# CDC means Contextual Deliberation Component
all_cdc = [ContextualDeliberationComponent(0, ['Test'])]  # This is a sorted list based on computational_effort
all_cdc.pop()
all_cdc.append(CC_minimal_old())
all_cdc.append(CC_repetition())
all_cdc.append(DC_default_action())
all_cdc.append(DC_goal_from_context())
all_cdc.append(DC_goal_from_imitation())
all_cdc.append(DC_plan_making())
all_cdc.append(DC_end())

in_dc = all_cdc
current_dc = None
out_dc = []


class Deliberator:

    def __init__(self):
        print("Initialized:" + type(self).__name__)
        self.currentContext = Context()

    def main_deliberate(self):
        print("-------------------------------------")
        print("Start deliberating")
        self.currentContext.clear()
        act_or_crit = DelibFocus.CONTEXT_EXPANSION
        while True:
            print("-------------------------------------")
            cdc = self.select_cdc([act_or_crit])

            remove_from_in = False
            print()
            if issubclass(type(cdc), ContextualComponent):
                act_or_crit, remove_from_in = cdc.explore_context(self.currentContext)
            elif issubclass(type(cdc), DeliberationComponent):
                act_or_crit, remove_from_in = cdc.deliberate(self.currentContext)

            if remove_from_in: self.remove_dc(cdc)

            if type(act_or_crit) == Action:
                print("Perform action: " + act_or_crit.effect)
                break
            if type(act_or_crit) == DelibFocus:
                print("Deliberate more: " + act_or_crit.name)
        print("End deliberating")
        print("-------------------------------------")

    def select_cdc(self, new_criteria: list) -> ContextualDeliberationComponent:
        prt = "Select DC [Crt: " + new_criteria[0].name + "]"
        selected_dc = DC_end()
        for s_dc in in_dc:
            if s_dc.check_criteria(new_criteria):
                selected_dc = s_dc
                prt += ": " + s_dc.name()
                break
        print(prt)
        return selected_dc

    def remove_dc(self, delib_aid):
        print("Remove dc: " + str(type(delib_aid)))
        out_dc.append(delib_aid)
        in_dc.remove(delib_aid)
