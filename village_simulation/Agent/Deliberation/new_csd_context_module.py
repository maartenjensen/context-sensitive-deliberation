from village_simulation.Agent.Data.the_agent import Human
from village_simulation.Agent.Data.enums import Days, Activity
from village_simulation.Common.sim_utils import SimUtils

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

    def explore_context(self, agent: Human):
        self.time = self.get_time()
        self.day = self.get_day()
        self.time_based_activity = self.get_time_based_activity(agent)

    def get_time(self) -> int:
        return SimUtils.get_model().get_time()

    def get_day(self) -> Days:
        return SimUtils.get_model().get_day()

    def get_time_based_activity(self, agent: Human):
        return agent.schedule_time.get_activity_based_on_time(self.time, self.day)

    def print_context(self):
        print(str(self.day) + " " + str(self.time) + ":00 " + str(self.time_based_activity))
