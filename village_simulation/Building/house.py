from village_simulation.Building.location import Location
from village_simulation.Model.model_params import Constants


class House(Location):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos, (3, 3), '#aabcf2', Constants.layer_buildings)
        print("Added a house " + str(unique_id))

        self.beef = 0
        self.chicken = 0
        self.tofu = 0

    def to_str(self):
        info = "House " + str(self.unique_id) + ","
        # info += "B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        # From now agents just hold their own food with them
        return info
