from village_simulation.Building.location import Location
from village_simulation.Model.model_parent import ParentModel
from village_simulation.Model.params import Constants


class TimeIndicator(Location):

    def __init__(self, unique_id, model: ParentModel, pos):
        super().__init__(unique_id, model, pos, (1, 1), '#cf9393', Constants.layer_base)

    def to_str(self):
        if isinstance(self.model, ParentModel):

            info = str(self.model.schedule.steps) + " "
            day = self.model.get_day_n()
            days = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
            info += days[day]
            info += " {:.2f}".format(self.model.get_time_day())
            return info

        return "Error"
