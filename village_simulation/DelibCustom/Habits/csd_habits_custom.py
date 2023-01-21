from village_simulation.EComponentsS.simulation_enums import Activity, Goal, DefaultFood
from village_simulation.EntitiesCS.the_agent import Human


class a:

    def add_habit_sleeping(self):

        self.dc.add_node(Activity.SLEEP)
        self.dc.add_node_and_edge(self.actSleep, Activity.SLEEP)

    def add_habit_eat(self, agent: Human):

        self.dc.add_node(Activity.EAT)
        self.dc.add_node_and_edge(Goal.EAT_FOOD, Activity.EAT)
        if agent.food.default_food == DefaultFood.BEEF:
            self.dc.add_node_and_edge(self.actEatBeef, Activity.EAT)
        elif agent.food.default_food == DefaultFood.CHICKEN:
            self.dc.add_node_and_edge(self.actEatChicken, Activity.EAT)
        elif agent.food.default_food == DefaultFood.TOFU:
            self.dc.add_node_and_edge(self.actEatTofu, Activity.EAT)
        self.dc.add_edge(self.actEatChicken, Goal.EAT_FOOD)

    def set_habit_work(self):

        self.dc.add_node(Activity.WORK)
        self.dc.add_node_and_edge(self.actWork, Activity.WORK)

    def set_habit_buy_food(self):

        self.dc.add_node(Activity.BUY_FOOD)
        self.dc.add_node_and_edge(self.actBuyFood, Activity.BUY_FOOD)

    def set_habit_leisure(self):

        self.dc.add_node(Activity.LEISURE)
        self.dc.add_node_and_edge(self.actRelax, Activity.LEISURE)