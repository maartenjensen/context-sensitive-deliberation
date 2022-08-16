# My classes
from old_csd_framework.csd_contextual_deliberation_components import *
from old_csd_framework.csd_context import *

cef_all = [ContextExpansionFunction(0, ['Test'])]  # This is a sorted list based on computational_effort
cef_all.pop()
cef_all.append(CC_minimal())
cef_all.append(CC_affordances())
cef_all.append(CC_affordances_people())
cef_all.append(CC_imitate_action())
cef_all.append(CC_imitate_goal())
cef_all.append(CC_end())

# CDC means Contextual Deliberation Component
dc_all = [DeliberationComponent(0, ['Test'])]  # This is a sorted list based on computational_effort
dc_all.pop()
dc_all.append(DC_default_action())

# all_cdc.append(DC_goal_from_context())
# all_cdc.append(DC_goal_from_imitation())
# all_cdc.append(DC_plan_making())

class Deliberator:

    def __init__(self):
        print("Initialized:" + type(self).__name__)
        self.currentContext = CurrentContext()

        self.cef_in = cef_all
        self.cef_out = []

        self.dc_in = dc_all
        self.dc_out = []

    def main_deliberate(self):
        print("-------------------------------------")
        print("Start deliberating")
        self.currentContext.clear()
        self.currentContext.print_relevant_context()
        act_or_focus_list = [DelibFocus.CONTEXT_EXPANSION]
        while True:
            print("-------------------------------------")
            # before CEF and DC lists are empty a decision should have been made
            if len(self.cef_in) == 0 and len(self.dc_in) == 0:
                print("ERRRRRRRROOOOOOOORR")
            elif len(self.dc_in) == 0:
                self.reset_dc_list()
                act_or_focus_list = [DelibFocus.CONTEXT_EXPANSION]
                print("No deliberation applicable, changing to expanding context")

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
        selected_dc = DeliberationComponent(0, ['Test'])
        selected_dc = DC_end()
        for t_dc in self.dc_in:
            if t_dc.check_criteria(new_criteria):
                selected_dc = t_dc
                prt += ": " + t_dc.name()
                break
        print(prt)
        return selected_dc

    def select_context_expansion_function(self, new_criteria: list) -> ContextExpansionFunction:
        prt = "Select CEF [Focus: " + new_criteria[0].name + "]"
        selected_cef = ContextExpansionFunction(0, ['Test'])
        selected_cef = CC_end()
        for t_cef in self.cef_in:
            if t_cef.check_criteria(new_criteria):
                selected_cef = t_cef
                prt += ": " + t_cef.name()
                break
        print(prt)
        return selected_cef

    def remove_dc(self, delib_component):
        print("Remove dc: " + str(type(delib_component)))
        self.dc_out.append(delib_component)
        self.dc_in.remove(delib_component)

    def remove_cef(self, context_function):
        print("Remove cef: " + str(type(context_function)))
        self.cef_out.append(context_function)
        self.cef_in.remove(context_function)

    def reset_dc_list(self):
        self.dc_in = dc_all
        self.dc_out = []

    def reset_cef_list(self):
        self.cef_in = cef_all
        self.cef_out = []