import mesa

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

        # Create agents
        for i in range(self.num_agents):
            a = MyAgent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = mesa.DataCollector(model_reporters={"Avg food": compute_avg_food},
                                                agent_reporters={"Money": "money", "Food": "food"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

from csd_framework.csd_deliberator import Deliberator

class MyAgent(mesa.Agent):
    """An agent with some money"""

    def __init__(self, unique_id, model: MesaShoppingModel):
        super().__init__(unique_id, model)
        self.model = model
        self.money = 50
        self.food = 20
        # Input model of context
        self.myDeliberator = Deliberator()

    def action_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        # Input context sensitive deliberation
        print("#####################################")
        print("Agent " + str(self.unique_id) + " deliberates")
        self.myDeliberator.main_deliberate()
        print("#####################################")