from village_simulation.Agent.Data.the_agent import HumanParent
from village_simulation.Agent.Data.enums import LocationEnum, DefaultFood
from village_simulation.Building.house import House
from village_simulation.Building.shop import Shop
from village_simulation.Model.model_parent import ParentModel

""" The ContextModule serves as a bridge between the information 
    of the simulation and the context-sensitive deliberation module.
    It uses a context ontology to change variables to context readable variables.
"""
class ContextModule:

    def get_location(self, agent: HumanParent):
        if agent.location == agent.my_house:
            return LocationEnum.HOME
        elif isinstance(agent.location, House):
            return LocationEnum.HOUSE
        elif isinstance(agent.location, Shop):
            return LocationEnum.SHOP
        else:
            return LocationEnum.OUTSIDE

    # time is indicated in hours
    def get_time(self, model: ParentModel):
        n_steps = model.schedule.steps
        time = n_steps % model.time_hours_day
        return time

    def get_activity(self, agent: HumanParent):
        return agent.activity

    def get_plan(self, agent: HumanParent):
        return agent.plan

    def get_need(self, agent: HumanParent):
        return agent.need

    def get_goal(self, agent: HumanParent):
        return agent.goal

    def get_default_food(self, agent: HumanParent, model: ParentModel):
        # this should be replaced by a function that takes the people around this person and then the most liked food
        return DefaultFood.TOFU