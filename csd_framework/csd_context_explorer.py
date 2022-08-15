from csd_framework.csd_context_module import ContextModule
from village_simulation.Agents.agents_parent import ParentAgent


class ContextExplorer:

    def __init__(self):

        self.cm = ContextModule()

    def get_primary_information(self, agent: ParentAgent):

        string = str(self.cm.get_location(agent))
        if self.cm.get_activity(agent).value > -1:
            string += ", activity: " + str(self.cm.get_activity(agent))
        if self.cm.get_plan(agent).value > -1:
            string += ", plan: " + str(self.cm.get_activity(agent))
        if self.cm.get_need(agent).value > -1:
            string += ", need: " + str(self.cm.get_need(agent))
        if self.cm.get_goal(agent).value > -1:
            string += ", goal: " + str(self.cm.get_goal(agent))

        return string
