from new_csd_framework.csd_context_explorer import ContextExplorer
from new_csd_framework.csd_context_ontology import DefaultFood
from old_csd_framework.csd_deliberator import Deliberator
from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Agents.buildings import House
from village_simulation.Agents.enums import Activity, Plan, Need, Goal
from village_simulation.Model.model_parent import ParentModel


class MyAgent(ParentAgent):
    """An agent with some money"""

    def __init__(self, unique_id, model: ParentModel, pos, my_house: House):
        super().__init__(unique_id, model)
        # Variables
        self.model = model
        self.pos = pos
        self.my_house = my_house
        self.location = None
        self.has_bike = self.model.random.getrandbits(1)
        self.has_car = self.model.random.getrandbits(1)
        self.money = 50
        self.beef = self.model.random.randint(0, 5)
        self.chicken = self.model.random.randint(0, 5)
        self.tofu = self.model.random.randint(0, 5)

        # Default food
        self.default_food = DefaultFood.BEEF
        if self.chicken > self.beef:
            self.default_food = DefaultFood.CHICKEN
        if self.tofu > self.chicken and self.tofu > self.beef:
            self.default_food = DefaultFood.TOFU

        # Utility
        self.ut_beef = self.beef
        self.ut_chicken = self.chicken
        self.ut_tofu = self.tofu

        # Enums
        self.activity = Activity.RELAXING
        self.plan = Plan.NONE
        self.need = Need.NONE
        self.goal = Goal.NONE

        # Complex variables
        self.my_deliberator = Deliberator()
        self.context_explorer = ContextExplorer()

        # Functions
        self.model.schedule.add(self)
        self.move_to_house()

    def action_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        # Input context sensitive deliberation
        print("#####################################")
        print("Agent " + str(self.unique_id) + " retrieves context")
        #print(self.context_explorer.get_primary_information(self, self.model))
        self.context_explorer.get_primary_information(self, self.model)
        print(self.context_explorer.print_primary_information())
        chosen_food = self.context_explorer.deliberate(self, self.model)
        if chosen_food == DefaultFood.BEEF:
            self.eat_beef()
        elif chosen_food == DefaultFood.CHICKEN:
            self.eat_chicken()
        elif chosen_food == DefaultFood.TOFU:
            self.eat_tofu()

        # self.my_deliberator.main_deliberate()
        print("#####################################")

    def move_to_house(self):
        self.pos = self.my_house.get_random_position_on()
        self.model.grid.place_agent(self, self.pos)
        self.location = self.my_house

    def get_food(self):
        return self.beef + self.chicken + self.tofu

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", "
        info += "Money: " + str(self.money)
        if self.has_car:
            info += ", Car"
        if self.has_bike:
            info += ", Bike"
        info += ", B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        return info

    """ ACTIONS """
    def eat_beef(self):
        if self.beef > 0:
            self.beef -= 1
            print("eating beef")
        else:
            print("ERROR")

    def eat_chicken(self):
        if self.chicken > 0:
            self.chicken -= 1
            print("eating chicken")
        else:
            print("ERROR")

    def eat_tofu(self):
        if self.tofu > 0:
            self.tofu -= 1
            print("eating tofu")
        else:
            print("ERROR")