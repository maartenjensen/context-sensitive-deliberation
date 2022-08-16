from new_csd_framework.csd_context_module import ContextModule
from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Model.model_parent import ParentModel


class ContextExplorer:

    def __init__(self):

        self.cm = ContextModule()

    def get_primary_information(self, agent: ParentAgent, model: ParentModel):

        string = str(self.cm.get_location(agent))
        string += ", Time:" + str(self.cm.get_time(model))
        if self.cm.get_activity(agent).value > -1:
            string += ", " + str(self.cm.get_activity(agent))
        if self.cm.get_plan(agent).value > -1:
            string += ", " + str(self.cm.get_activity(agent))
        if self.cm.get_need(agent).value > -1:
            string += ", " + str(self.cm.get_need(agent))
        if self.cm.get_goal(agent).value > -1:
            string += ", " + str(self.cm.get_goal(agent))

        return string
