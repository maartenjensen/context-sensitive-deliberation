import mesa

from village_simulation.Model.sim_utils import SimUtils


class Location(mesa.Agent):
    """Agent"""

    def __init__(self, unique_id, model, pos, dim, color, layer):
        super().__init__(unique_id, model)
        self.pos = pos
        self.dim = dim
        self.color = color
        self.layer = layer

        SimUtils.get_model().schedule.add(self)
        SimUtils.get_model().grid.place_agent(self, self.pos)

    def step(self):
        a = 1 + 1

    def get_random_position_on(self):
        x = self.pos[0] - SimUtils.get_model().random.randint(0, self.dim[0] - 1)
        y = self.pos[1] + SimUtils.get_model().random.randint(0, self.dim[1] - 1)
        return x, y

    def to_str(self):
        return str(self.unique_id)


