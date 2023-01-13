from village_simulation.Building.location import Location
from village_simulation.Model.model_params import Constants


class Shop(Location):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos, (7, 3), '#badbc6', Constants.layer_buildings)
        print("Added a shop " + str(unique_id))

        self.beef = 100
        self.chicken = 100
        self.tofu = 100

    def step(self):
        self.beef += 1
        self.chicken += 1
        self.tofu += 1

    def to_str(self):
        info = "Shop " + str(self.unique_id) + ", \n"
        # Not necessary, can open up again when not having food in a shop becomes relevant.
        # info += "B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        return info
