from village_simulation.Agent.agents_parent import ParentAgent
from village_simulation.Agent.enums import Location, DefaultFood
from village_simulation.Building.buildings import Shop, House
from village_simulation.Model.model_parent import ParentModel

""" The ContextModule serves as a bridge between the information 
    of the simulation and the context-sensitive deliberation module.
    It uses a context ontology to change variables to context readable variables.
"""
class ContextModule:

    def get_location(self, agent: ParentAgent):
        if agent.location == agent.my_house:
            return Location.HOME
        elif isinstance(agent.location, House):
            return Location.HOUSE
        elif isinstance(agent.location, Shop):
            return Location.SHOP
        else:
            return Location.OUTSIDE

    # time is indicated in hours
    def get_time(self, model: ParentModel):
        n_steps = model.schedule.steps
        time = n_steps % model.time_hours_day
        return time

    def get_activity(self, agent: ParentAgent):
        return agent.activity

    def get_plan(self, agent: ParentAgent):
        return agent.plan

    def get_need(self, agent: ParentAgent):
        return agent.need

    def get_goal(self, agent: ParentAgent):
        return agent.goal

    def get_default_food(self, agent: ParentAgent, model: ParentModel):
        # this should be replaced by a function that takes the people around this person and then the most liked food
        return DefaultFood.TOFU