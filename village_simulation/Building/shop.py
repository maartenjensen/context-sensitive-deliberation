from village_simulation.Building.location import Location
from village_simulation.Model.params import Constants


class Shop(Location):

    def __init__(self, unique_id, model, pos, neighborhood):
        super().__init__(unique_id, model, pos, (5, 5), '#badbc6', Constants.layer_buildings)
        print("Added a shop " + str(unique_id))

        self.neighborhood = neighborhood

        self.beef = 100
        self.chicken = 100
        self.tofu = 100

    def step(self):
        self.beef += 1
        self.chicken += 1
        self.tofu += 1

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", \n"
        info += "B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        return info
