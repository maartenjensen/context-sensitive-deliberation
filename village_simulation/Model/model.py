import math

import mesa

from village_simulation.Deliberation.csd_deliberator import Deliberator
from village_simulation.EntitiesCS.the_agent import Human
from village_simulation.EComponentsS.enums import Days, DayType
from village_simulation.ECSystems.sys_deliberation import SysDeliberation
from village_simulation.ECSystems.sys_needs import SysNeeds
from village_simulation.Model.model_parent import ParentModel
from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Model.model_builder import VillageBuilder


def compute_avg_food(model):
    agent_foods = 0
    agent_n = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Human):
            agent_foods += agent.food.get_total_food()
            agent_n += 1
    return agent_foods / agent_n


def compute_avg_delib_cost(model):
    agent_delib_cost = 0
    agent_n = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Human):
            agent_delib_cost += agent.deliberation.delib_cost
            agent_n += 1
    return agent_delib_cost / agent_n


class ShoppingModel(ParentModel):
    """A model with some agents"""

    def __init__(
            self,
            world_cell_px,
            world_w_cell,
            world_h_cell,
            n_agents,
            n_houses,
            n_shops,
            n_offices,
            n_neighborhoods,
            time_days,
            time_hours_day,
            time_steps_day
    ):
        # Initialize model settings
        super().__init__()

        # Set self as SimUtils model
        SimUtils.set_model(self)

        self.world_cell_px = world_cell_px
        self.world_w_cell = world_w_cell
        self.world_h_cell = world_h_cell
        self.num_agents = n_agents
        self.n_houses = n_houses
        self.n_shops = n_shops
        self.n_offices = n_offices
        self.n_neighborhoods = n_neighborhoods
        self.time_days = time_days
        self.time_hours_day = time_hours_day
        self.time_steps_day = time_steps_day

        self.grid = mesa.space.MultiGrid(world_w_cell, world_h_cell, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        village_builder = VillageBuilder()
        village_builder.build_buildings(self.n_houses, self.n_shops, self.n_offices, self.n_neighborhoods)
        village_builder.spawn_agents(self.num_agents)
        village_builder.make_some_agents_stupid()
        village_builder.print_humans()

        self.datacollector = mesa.DataCollector(model_reporters={"Avg food": compute_avg_food, "Avg delib cost": compute_avg_delib_cost},
                                                agent_reporters={"Money": lambda a: getattr(a, "money", None),
                                                                 "Food": lambda a: getattr(a, "beef", None)})

    def step(self):
        self.day_type_update()
        self.schedule.step()
        self.agents_step()
        self.datacollector.collect(self)

    def day_type_update(self):
        """ Simplified function that changes the day type at the start of the day, step == 0 """
        if self.start_of_day():
            if self.day_type == DayType.WORK:
                self.day_type = DayType.WEEKEND
            else:
                self.day_type = DayType.WORK

    def agents_step(self):

        deliberator = Deliberator()

        print("#####################################")
        for agent in self.schedule.agent_buffer(shuffled=True):

            if isinstance(agent, Human):
                print("Updating needs " + str(agent.unique_id))
                SysNeeds.update_needs(agent.needs, agent.economy, agent.food, self.get_time_day(), self.time_steps_day)

        for agent in self.schedule.agent_buffer(shuffled=True):

            if isinstance(agent, Human):
                print("#####################################")
                print("Agent " + str(agent.unique_id) + " is deliberating")
                deliberator.deliberate(agent)  # the deliberator performs an action for the agent
                agent.deliberation.print()

        print("#####################################")

        for agent in self.schedule.agent_buffer(shuffled=True):

            if isinstance(agent, Human):
                SysDeliberation.clear_deliberation(agent.deliberation)

    """ Represent time in float, see if that works otherwise change back to int """

    def start_of_day(self) -> bool:
        n_steps = self.schedule.steps
        step_in_day = n_steps % self.time_steps_day
        return step_in_day == 0

    def get_time_day(self) -> float:
        n_steps = self.schedule.steps
        time = (n_steps % self.time_steps_day) / (self.time_steps_day / self.time_hours_day)
        return time

    def get_hour(self) -> int:
        n_steps = self.schedule.steps
        time = (n_steps - (n_steps % 4)) / 4
        return time

    def get_day(self) -> Days:

        days = {0: Days.MO, 1: Days.TU, 2: Days.WE, 3: Days.TH, 4: Days.FR, 5: Days.SA, 6: Days.SU}
        return days[self.get_day_n()]

    def get_day_n(self) -> int:

        n_steps = self.schedule.steps
        day = math.floor(n_steps / self.time_steps_day) % self.time_days

        return day
