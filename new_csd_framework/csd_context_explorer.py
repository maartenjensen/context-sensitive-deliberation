from new_csd_framework.csd_context_module import ContextModule
from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Agents.enums import Activity, Plan, Need, Goal
from village_simulation.Model.model_parent import ParentModel
from new_csd_framework.csd_context_ontology import Location, DefaultFood

class ContextExplorer:

    def __init__(self):

        self.cm = ContextModule()
        self._0_location = Location.NONE
        self._0_time = -1
        self._0_activity = Activity.RELAXING
        self._0_plan = Plan.NONE
        self._0_need = Need.NONE
        self._0_goal = Goal.NONE


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

    def deliberate_on_primary_information(self, agent: ParentAgent, model: ParentModel):

        time = self.cm.get_time(model)
        if time == 6:
            return agent.default_food
        elif time == 12:
            return agent.default_food
        elif time == 18:
            return agent.default_food
        return agent.default_food.NONE