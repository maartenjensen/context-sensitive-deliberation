import mesa
from mesa_simulation.sim_agent import MyAgent, MyLocation

def compute_avg_food(model):
    agent_foods = [agent.food for agent in model.schedule.agents]
    return sum(agent_foods) / len(agent_foods)

class MesaShoppingModel(mesa.Model):
    """A model with some agents"""

    def __init__(self, n_agents, width, height):
        # Initialize model settings
        super().__init__()
        self.num_agents = n_agents
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        unique_id = 0
        # Create agents
        for i in range(self.num_agents):
            a = MyAgent(unique_id, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            unique_id += 1

        # Create locations
        for i in range(5):
            loc = MyLocation(unique_id, self)
            self.schedule.add(loc)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(loc, (x, y))
            unique_id += 1

        self.datacollector = mesa.DataCollector(model_reporters={"Avg food": compute_avg_food},
                                                agent_reporters={"Money": "money", "Food": "food"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

