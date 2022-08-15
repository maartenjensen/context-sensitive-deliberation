import mesa

from village_simulation.Agents.agents import MyAgent
from village_simulation.Model.model_parent import MesaParentModel
from village_simulation.village_builder import VillageBuilder

def compute_avg_food(model):
    agent_foods = 0
    agent_n = 0
    for agent in model.schedule.agents:
        if isinstance(agent, MyAgent):
            agent_foods += agent.get_food()
            agent_n += 1
    return agent_foods / agent_n


class MesaShoppingModel(MesaParentModel):
    """A model with some agents"""

    def __init__(
            self,
            world_cell_px,
            world_w_cell,
            world_h_cell,
            n_agents,
            n_houses,
            n_shops,
            n_neighborhoods
    ):
        # Initialize model settings
        super().__init__()
        self.world_cell_px = world_cell_px
        self.world_w_cell = world_w_cell
        self.world_h_cell = world_h_cell
        self.num_agents = n_agents
        self.n_houses = n_houses
        self.n_shops = n_shops
        self.n_neighborhoods = n_neighborhoods

        self.grid = mesa.space.MultiGrid(world_w_cell, world_h_cell, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        village_builder = VillageBuilder(self, self.grid, self.schedule, self.random)
        village_builder.build_buildings(self.n_houses, self.n_shops, self.n_neighborhoods)
        village_builder.spawn_agents(self.num_agents)

        self.datacollector = mesa.DataCollector(model_reporters={"Avg food": compute_avg_food},
                                                agent_reporters={"Money": lambda a: getattr(a, "money", None),
                                                                 "Food": lambda a: getattr(a, "beef", None)})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
