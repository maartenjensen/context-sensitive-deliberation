from new_csd_framework.new_csd_context_module import ContextTimeActivity
from village_simulation.Agent.agents_parent import ParentAgent
from village_simulation.Agent.enums import Activity
from village_simulation.Model.model_parent import ParentModel

""" The deliberator class contains all the deliberation functions, it explores the context and calls
    the deliberation functions to help with decision making """

class Deliberator:

    def __init__(self):
        print("Initialize Context modules")
        self.CTimeActivity = ContextTimeActivity()

    def deliberate(self, agent: ParentAgent, model: ParentModel):

        self.CTimeActivity.explore_context(agent, model)
        self.CTimeActivity.print_context()

        action = self.get_action_from_activity(agent, self.CTimeActivity.time_based_activity)
        if action != agent.actions.none_action:
            return action
        else:
            print("Good the program works, a none_action has been returned")
            return action

    def get_action_from_activity(self, agent: ParentAgent, activity):

        if activity == Activity.SLEEP:
            return agent.actions.sleep
        elif activity == Activity.WORK:
            return agent.actions.work
        elif activity == Activity.EAT:
            return agent.actions.none_action
        elif activity == Activity.EAT_BEEF:
            return agent.actions.eat_beef
        elif activity == Activity.EAT_CHICKEN:
            return agent.actions.eat_chicken
        elif activity == Activity.EAT_TOFU:
            return agent.actions.eat_tofu

        return agent.actions.none_action
