# My classes
from csd_framework.csd_contextual_deliberation_components import *
from csd_framework.csd_context import *

# CDC means Contextual Deliberation Component
all_dc = [DeliberationComponent(0, ['Test'])]  # This is a sorted list based on computational_effort
all_dc.pop()
all_dc.append(DC_default_action())
#all_cdc.append(DC_goal_from_context())
#all_cdc.append(DC_goal_from_imitation())
#all_cdc.append(DC_plan_making())
#all_cdc.append(DC_end())

all_cef = [ContextExpansionFunction(0, ['Test'])]  # This is a sorted list based on computational_effort
all_cef.pop()
all_cef.append(CC_minimal())
all_cef.append(CC_affordances())
all_cef.append(CC_affordances_people())
all_cef.append(CC_imitate_action())
all_cef.append(CC_imitate_goal())
all_cef.append(CC_end())

in_dc = all_dc
current_dc = None
out_dc = []

in_cef = all_cef
current_cef = None
out_cef = []

class Deliberator:

    def __init__(self):
        print("Initialized:" + type(self).__name__)
        self.currentContext = CurrentContext()

    def main_deliberate(self):
        print("-------------------------------------")
        print("Start deliberating")
        self.currentContext.clear()
        self.currentContext.print_relevant_context()
        act_or_focus_list = [DelibFocus.CONTEXT_EXPANSION]
        while True:
            print("-------------------------------------")
            if act_or_focus_list[0] == DelibFocus.CONTEXT_EXPANSION:
                cef = self.select_context_expansion_function(act_or_focus_list)
                act_or_focus_list, remove_from_in = cef.explore_context(self.currentContext)
                self.currentContext.print_relevant_context()
                if remove_from_in:
                    self.remove_cef(cef)
            else:
                dc = self.select_deliberation_component(act_or_focus_list)
                act_or_focus_list, remove_from_in = dc.deliberate(self.currentContext)
                if remove_from_in:
                    self.remove_dc(dc)

            if type(act_or_focus_list[0]) == Action:
                print("Perform action: " + str(act_or_focus_list[0]))
                break
            if type(act_or_focus_list[0]) == DelibFocus:
                print("Deliberate more: " + str(act_or_focus_list[0]))

        print("End deliberating")
        print("-------------------------------------")

    def select_deliberation_component(self, new_criteria: list) -> DeliberationComponent:
        prt = "Select DC [Focus: " + new_criteria[0].name + "]"
        selected_dc = DC_end()
        for t_dc in in_dc:
            if t_dc.check_criteria(new_criteria):
                selected_dc = t_dc
                prt += ": " + t_dc.name()
                break
        print(prt)
        return selected_dc

    def select_context_expansion_function(self, new_criteria: list) -> ContextExpansionFunction:
        prt = "Select CEF [Focus: " + new_criteria[0].name + "]"
        selected_cef = CC_end()
        for t_cef in in_cef:
            if t_cef.check_criteria(new_criteria):
                selected_cef = t_cef
                prt += ": " + t_cef.name()
                break
        print(prt)
        return selected_cef

    def remove_dc(self, delib_component):
        print("Remove dc: " + str(type(delib_component)))
        out_dc.append(delib_component)
        in_dc.remove(delib_component)

    def remove_cef(self, context_function):
        print("Remove cef: " + str(type(context_function)))
        out_cef.append(context_function)
        in_cef.remove(context_function)
