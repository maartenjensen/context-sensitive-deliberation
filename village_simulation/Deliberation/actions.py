from village_simulation.EComponentsS.enums import CarTypes
from village_simulation.EntitiesCS.the_agent import Human
from village_simulation.ECSystems.sys_food import SysFood
from village_simulation.ECSystems.sys_position import SysPosition
from village_simulation.ECSystems.sys_time_schedule import SysScheduleTime


class Action:

    def __init__(self, steps_active=0):
        self.steps_active = steps_active

    def check_preconditions(self, agent: Human) -> bool:
        print("Preconditions checked and accepted")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("Executed action")
        return True

    def action_step(self, agent: Human):
        self.steps_active -= 1
        if self.steps_active == 0:
            self.execute_action(agent)


class ActNone(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Should not be called")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("This function should not even be called")
        return True


class ActChill(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return agent.position.at_home()

    def execute_action(self, agent: Human) -> bool:
        print("The agent just chilled")
        return True


class ActSleep(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return agent.position.at_home()

    def execute_action(self, agent: Human) -> bool:
        print("The agent slept")
        agent.needs.sleep -= 0.5
        return True


class ActWork(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at work")
        return agent.position.at_work()

    def execute_action(self, agent: Human) -> bool:
        print("The agent worked")
        agent.needs.work -= 0.5
        return True


class ActEatBeef(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has beef")
        return agent.food.beef > 0

    def execute_action(self, agent: Human) -> bool:

        if agent.food.beef > 0:
            agent.food.beef -= 1
            agent.needs.sleep = 0
            print("Eating beef")
            return True
        else:
            print("ERROR")
            return False


class ActEatChicken(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has chicken")
        return agent.food.chicken > 0

    def execute_action(self, agent: Human) -> bool:

        if agent.food.chicken > 0:
            agent.food.chicken -= 1
            agent.needs.sleep = 0
            print("Eating chicken")
            return True
        else:
            print("ERROR")
            return False


class ActEatTofu(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has tofu")
        return agent.food.tofu > 0

    def execute_action(self, agent: Human) -> bool:

        if agent.food.tofu > 0:
            agent.food.tofu -= 1
            agent.needs.sleep = 0
            print("Eating tofu")
            return True
        else:
            print("ERROR")
            return False


class ActTravelToWork(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is not already at work")
        return not agent.position.at_work()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            SysPosition.move_to_office(agent.position)
            print("Moving to office")
            return True
        else:
            print("ERROR")
            return False


class ActTravelToHome(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is not already at home")
        return not agent.position.at_home()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            SysPosition.move_to_house(agent.position)
            print("Moving to home")
            return True
        else:
            print("ERROR")
            return False


class ActTravelToShop(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is not already at the shop")
        return not agent.position.at_shop()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            SysPosition.move_to_shop(agent.position)
            print("Moving to shop")
            return True
        else:
            print("ERROR")
            return False


class ActBuyFood(Action):

    def __init__(self, amount_beef, amount_chicken, amount_tofu):

        super().__init__()
        self.amount_beef = amount_beef
        self.amount_chicken = amount_chicken
        self.amount_tofu = amount_tofu

    def get_food_cost(self):

        # This should actually be retrieved from the store
        return self.amount_beef + self.amount_chicken + self.amount_tofu

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is at the shop and has enough money")
        if not agent.position.at_shop():
            print("Agent not at the shop")
            return False
        return agent.economy.money >= self.get_food_cost()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            SysFood.add_food(agent.food, self.amount_beef, self.amount_chicken, self.amount_tofu)
            agent.economy.money -= self.get_food_cost()
            print("Buy food: B:" + str(self.amount_beef) + ", C:" + str(self.amount_chicken) + ", T:" + str(
                self.amount_tofu))
            return True
        else:
            print("ERROR")
            return False


class ActBuyCar(Action):

    def __init__(self, car_type: CarTypes):

        super().__init__()
        self.carType = car_type

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has enough savings")
        return True

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            SysScheduleTime.custom_overwrite_bought_a_car(agent.schedule_time)
            # Add the car to possession and change the savings to right amount
            agent.economy.savings -= 40000
            print("Agent " + str(agent.unique_id) + " bought a " + str(self.carType))
            return True
        else:
            print("ERROR")
            return False
