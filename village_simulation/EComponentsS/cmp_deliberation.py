from village_simulation.EComponentsS.enums import Activity


class CmpDeliberation:

    def __init__(self):

        self.current_activity = Activity.NONE
        self.current_action = None  # I should find a solution for this because this is an Actions object
        self.delib_cost = 1

    def print(self):
        if self.current_action is not None:
            print("Activity: " + str(self.current_activity) + ", chosen action: " + self.current_action.to_string())
        else:
            print("Activity: " + str(self.current_activity) + ", chosen action: None")
