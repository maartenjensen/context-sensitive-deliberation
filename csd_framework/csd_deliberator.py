# My classes
from csd_framework.csd_deliberation_components import *
from csd_framework.csd_context import *

all_dc = [DeliberationComponent(0, ['Test'])]  # This is a sorted list based on computational_effort
all_dc.pop()
all_dc.append(DC_default_action())
all_dc.append(DC_goal_from_context())
all_dc.append(DC_goal_from_imitation())
all_dc.append(DC_plan_making())
all_dc.append(DC_end())

in_dc = all_dc
current_dc = None
out_dc = list()


class Deliberator:

    def __init__(self):
        print("Initialized:" + type(self).__name__)
        self.currentContext = Context()

    def main_deliberate(self):
        print("-------------------------------------")
        print("Start deliberating")
        self.currentContext.clear()
        act_or_crit = Criteria.ACTION_FINDING
        while True:
            print("-------------------------------------")
            delib_aid = self.select_dc([act_or_crit])
            act_or_crit, remove_from_in = delib_aid.deliberate(self.currentContext)
            if remove_from_in: self.remove_dc(delib_aid)

            if type(act_or_crit) == Action:
                print("Perform action: " + act_or_crit.effect)
                break
            if type(act_or_crit) == Criteria:
                print("Deliberate more: " + act_or_crit.name)
        print("End deliberating")
        print("-------------------------------------")

    def select_dc(self, new_criteria: list) -> DeliberationComponent:
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
