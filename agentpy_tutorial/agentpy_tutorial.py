# https://agentpy.readthedocs.io/en/latest/overview.html

import agentpy as ap


class AgentpyModelSetup:

    def run_model(self):
        parameters = {
            'want_similar': 0.3,  # For agents to be happy
            'n_groups': 2,  # Number of groups
            'density': 0.95,  # Density of population
            'size': 50,  # Height and length of the grid
            'steps': 50  # Maximum number of steps
        }

        model = AgentpyShoppingModel(parameters)
        model.sim_setup()

        model.sim_step()
        model.sim_step()

        model.end()


class Person(ap.Agent):

    def setup(self):
        """ Initiate agent attributes. """
        self.grid = self.model.grid
        # self.random = self.model.random
        self.money = 10

    def buy_food(self):
        """ Be happy if rate of similar neighbors is high enough. """
        self.money = self.money - 1

    def find_new_home(self):
        """ Move to random free spot and update free spots. """
        new_spot = self.random.choice(self.model.grid.empty)
        self.grid.move_to(self, new_spot)


class AgentpyShoppingModel(ap.Model):

    def setup(self):
        # Parameters
        s = self.p.size
        n = self.n = int(self.p.density * (s ** 2))

        # Create grid and agents
        self.grid = ap.Grid(self, (s, s), track_empty=True)
        self.agents = ap.AgentList(self, n, Person)
        self.grid.add_agents(self.agents, random=True, empty=True)

    def update(self):  # For recording variables
        print("update()")

    def step(self):  # For changing variables
        # Let agents buy n
        print("step()")
        self.agents.buy_food()

    def get_money(self):
        return 100

    def end(self):
        # Measure segregation at the end of the simulation
        print("end()")
        self.report('Money', self.get_money())


"""----------------------
    AGENTPY Tutorial
----------------------"""
#from agentpy_tutorial.agentpy_tutorial import AgentpyModelSetup
agentpyModelSetup = AgentpyModelSetup()
agentpyModelSetup.run_model()