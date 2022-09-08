import math

from village_simulation.Agent.agents_parent import ParentAgent
from village_simulation.Agent.enums import Days, Activity
from village_simulation.Model.model_parent import ParentModel

""" These classes explore the context and has function to get the information out of the simulation"""
class NewContextModule:

    def __init__(self):
        """
        TODO Retrieve context from retrieve_context()
        """
        print("Init new context module")


class ContextTimeActivity(NewContextModule):

    def __init__(self):
        super().__init__()

        self.time = -1
        self.day = Days.NONE
        self.time_based_activity = Activity.NONE

    def explore_context(self, agent: ParentAgent, model: ParentModel):
        self.time = self.get_time(model)
        self.day = self.get_day(model)
        self.time_based_activity = self.get_time_based_activity(agent, model)

    def get_time(self, model: ParentModel) -> int:
        n_steps = model.schedule.steps
        time = n_steps % model.time_hours_day
        return time

    def get_day(self, model: ParentModel) -> Days:
        n_steps = model.schedule.steps
        day = math.floor(n_steps / model.time_hours_day) % model.time_days
        days = {0: Days.MO, 1: Days.TU, 2: Days.WE, 3: Days.TH, 4: Days.FR, 5: Days.SA, 6: Days.SU}
        return days[day]

    def get_time_based_activity(self, agent: ParentAgent, model: ParentModel):
        return agent.schedule.get_activity_based_on_time(self.time, self.day)

    def print_context(self):
        print(str(self.day) + " " + str(self.time) + ":00 " + str(self.time_based_activity))
