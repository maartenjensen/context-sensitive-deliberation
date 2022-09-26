import mesa

from village_simulation.Agent.enums import Days


class ParentModel(mesa.Model):

    def __init__(self):
        super().__init__()

        self.world_cell_px = 0
        self.world_w_cell = 0
        self.world_h_cell = 0
        self.num_agents = 0
        self.n_houses = 0
        self.n_shops = 0
        self.n_offices = 0
        self.n_neighborhoods = 0
        self.time_days = 0
        self.time_hours_day = 0

        self.grid = mesa.space.MultiGrid(10, 10, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

    def get_time(self) -> int:
        return -1

    def get_day(self) -> Days:
        return Days.NONE
