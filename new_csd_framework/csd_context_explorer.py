from new_csd_framework.csd_context_module import ContextModule
from village_simulation.Agents.actions import Actions
from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Agents.enums import Activity, Plan, Need, Goal
from village_simulation.Model.model_parent import ParentModel
from new_csd_framework.csd_context_ontology import Location, DefaultFood


class ContextExplorer:

    def __init__(self):

        self.cm = ContextModule()
        self.deliberation_functions = []
        self._0_location = Location.NONE
        self._0_time = -1
        self._0_activity = Activity.NONE
        self._0_plan = Plan.NONE
        self._0_need = Need.NONE
        self._0_goal = Goal.NONE

    def reset_primary_information(self):

        self._0_location = Location.NONE
        self._0_time = -1
        self._0_activity = Activity.NONE
        self._0_plan = Plan.NONE
        self._0_need = Need.NONE
        self._0_goal = Goal.NONE

    def get_primary_information(self, agent: ParentAgent, model: ParentModel):

        self.deliberation_functions = [self.deliberate_on_primary_information]
        self._0_location = self.cm.get_location(agent)
        self._0_time = self.cm.get_time(model)

        if self.cm.get_activity(agent).value > -1:
            self._0_activity = self.cm.get_activity(agent)
        if self.cm.get_plan(agent).value > -1:
            self._0_plan = self.cm.get_activity(agent)
        if self.cm.get_need(agent).value > -1:
            self._0_need = self.cm.get_need(agent)
        if self.cm.get_goal(agent).value > -1:
            self._0_goal = self.cm.get_goal(agent)

    def print_primary_information(self):

        string = ""
        if len(self.deliberation_functions) > 0:
            string += str(self.deliberation_functions)
        if self._0_location != Location.NONE:
            string += ", " + str(self._0_location)
        if self._0_time != -1:
            string += ", Time:" + str(self._0_time)
        if self._0_activity != Activity.NONE:
            string += ", " + str(self._0_activity)
        if self._0_plan != Plan.NONE:
            string += ", " + str(self._0_plan)
        if self._0_need != Need.NONE:
            string += ", " + str(self._0_need)
        if self._0_goal != Goal.NONE:
            string += ", " + str(self._0_goal)

        return string

    # Make some deliberation functions, context exploration also gives a list of deliberation function that can be tried
    def deliberate_on_primary_information(self, agent: ParentAgent, model: ParentModel):

        time = self._0_time
        chosen_food = DefaultFood.NONE

        if time == 6:
            chosen_food = agent.default_food
        elif time == 12:
            chosen_food = agent.default_food
        elif time == 18:
            chosen_food = agent.default_food

        if chosen_food == DefaultFood.NONE:
            return DefaultFood.NONE, False
        if chosen_food == DefaultFood.BEEF:
            return agent.actions.eat_beef, True
        if chosen_food == DefaultFood.CHICKEN:
            return agent.actions.eat_chicken, True
        if chosen_food == DefaultFood.TOFU:
            return agent.actions.eat_tofu, True

    def deliberate(self, agent: ParentAgent, model: ParentModel):

        for delib_func in self.deliberation_functions:
            action, succeeded = delib_func(agent, model)
            if succeeded:
                return action, True

        return agent.default_food.NONE, False

