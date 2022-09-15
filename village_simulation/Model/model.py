import math

import mesa

from village_simulation.Agent.Deliberation.csd_deliberator import Deliberator
from village_simulation.Agent.agents import Human
from village_simulation.Agent.enums import Days
from village_simulation.Model.model_parent import ParentModel
from village_simulation.Model.sim_utils import SimUtils
from village_simulation.village_builder import VillageBuilder


def compute_avg_food(model):
    agent_foods = 0
    agent_n = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Human):
            agent_foods += agent.food.get_food()
            agent_n += 1
    return agent_foods / agent_n


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
            n_neighborhoods,
            time_days,
            time_hours_day
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
        self.n_neighborhoods = n_neighborhoods
        self.time_days = time_days
        self.time_hours_day = time_hours_day

        self.grid = mesa.space.MultiGrid(world_w_cell, world_h_cell, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        village_builder = VillageBuilder()
        village_builder.build_buildings(self.n_houses, self.n_shops, self.n_neighborhoods)
        village_builder.spawn_agents(self.num_agents)

        self.datacollector = mesa.DataCollector(model_reporters={"Avg food": compute_avg_food},
                                                agent_reporters={"Money": lambda a: getattr(a, "money", None),
                                                                 "Food": lambda a: getattr(a, "beef", None)})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.agents_step()

    def agents_step(self):

        deliberator = Deliberator()

        for agent in self.schedule.agent_buffer(shuffled=True):

            if isinstance(agent, Human):
                print("#####################################")
                print("Agent " + str(agent.unique_id) + " retrieves context")
                chosen_action_object = deliberator.deliberate(agent)
                chosen_action_object.execute_action(agent)
                print("#####################################")

    def get_time(self) -> int:
        n_steps = self.schedule.steps
        time = n_steps % self.time_hours_day
        return time

    def get_day(self) -> Days:
        n_steps = self.schedule.steps
        day = math.floor(n_steps / self.time_hours_day) % self.time_days
        days = {0: Days.MO, 1: Days.TU, 2: Days.WE, 3: Days.TH, 4: Days.FR, 5: Days.SA, 6: Days.SU}
        return days[day]
