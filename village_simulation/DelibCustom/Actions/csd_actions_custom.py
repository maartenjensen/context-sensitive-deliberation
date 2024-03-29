from village_simulation.Common.sim_utils import SimUtils
from village_simulation.DelibFramework.csd_actions import Action
from village_simulation.ECSystems.sys_food import SysFood
from village_simulation.ECSystems.sys_position import SysPosition
from village_simulation.ECSystems.sys_time_schedule import SysScheduleTime
from village_simulation.EComponentsS.simulation_enums import DefaultFood, CarTypes
from village_simulation.EntitiesCS.the_agent import Human


class DefaultActionsContainer:

    def __init__(self):
        self.actNone = ActNone()
        self.actSleep = ActSleep()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()
        self.actWork = ActWork()
        self.actBuyFood = ActBuyFood(6, 6, 6)
        self.actRelax = ActRelax()
        self.actFootballGoalie = ActFootballGoalie()
        self.actFootballTeamplayer = ActFootballTeamplayer()
        self.actFootballSeriousPlayer = ActFootballSeriousPlayer()


class ActNone(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Should not be called")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("This function should not even be called")
        agent.deliberation.actions_list.append(self.to_string())
        return True


class ActRelax(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return True  # agent.position.at_home(), simplification, traveling is implicit

    def execute_action(self, agent: Human) -> bool:
        if not agent.position.at_home():  # Simplified because travel is implicit
            print("The agent moved home")
            SysPosition.move_to_house(agent.position)
        print("The agent just relaxed")
        agent.deliberation.actions_list.append(self.to_string())
        return True


class ActSleep(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return True  # agent.position.at_home(), simplification, traveling is implicit

    def execute_action(self, agent: Human) -> bool:
        if not agent.position.at_home():  # Simplified because travel is implicit
            print("The agent moved home")
            SysPosition.move_to_house(agent.position)
        print("The agent slept")
        agent.needs.sleep -= 0.5
        agent.needs.sleep = min(0, agent.needs.sleep)
        agent.deliberation.actions_list.append(self.to_string())
        return True


class ActWork(Action):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at work")
        return True  # agent.position.at_work(), simplified because travel is implicit

    def execute_action(self, agent: Human) -> bool:
        if not agent.position.at_work():  # Simplified because travel is implicit
            print("The agent moved to work")
            SysPosition.move_to_office(agent.position)
        print("The agent worked")
        agent.needs.work -= 0.5
        agent.economy.worked_hours_day += 2
        agent.deliberation.actions_list.append(self.to_string())
        return True


class ActEatBeef(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has beef")
        return agent.food.beef > 0

    def execute_action(self, agent: Human) -> bool:

        if not agent.position.at_home() and SimUtils.get_model().get_time_day() > 17:  # Have dinner at home
            print("The agent moved home")
        if agent.food.beef > 0:
            agent.food.beef -= 1
            agent.needs.hunger = 0
            print("Eating beef")
            agent.deliberation.actions_list.append(self.to_string())
            if agent.food.chicken > 0:
                agent.food.default_food = DefaultFood.BEEF
            return True
        else:
            print("ERROR")
            return False


class ActEatChicken(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has chicken")
        return agent.food.chicken > 0

    def execute_action(self, agent: Human) -> bool:

        if not agent.position.at_home() and SimUtils.get_model().get_time_day() > 17:  # Have dinner at home
            print("The agent moved home")
        if agent.food.chicken > 0:
            agent.food.chicken -= 1
            agent.needs.hunger = 0
            print("Eating chicken")
            agent.deliberation.actions_list.append(self.to_string())
            if agent.food.chicken > 0:
                agent.food.default_food = DefaultFood.CHICKEN
            return True
        else:
            print("ERROR")
            return False


class ActEatTofu(Action):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has tofu")
        return agent.food.tofu > 0

    def execute_action(self, agent: Human) -> bool:

        if not agent.position.at_home() and SimUtils.get_model().get_time_day() > 17:  # Have dinner at home
            print("The agent moved home")
        if agent.food.tofu > 0:
            agent.food.tofu -= 1
            agent.needs.hunger = 0
            print("Eating tofu")
            agent.deliberation.actions_list.append(self.to_string())
            if agent.food.chicken > 0:
                agent.food.default_food = DefaultFood.TOFU
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
            agent.deliberation.actions_list.append(self.to_string())
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
            agent.deliberation.actions_list.append(self.to_string())
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
            agent.deliberation.actions_list.append(self.to_string())
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
        # if not agent.position.at_shop(): # Simplified travelling
        #    print("Agent not at the shop")
        #    return False
        return agent.economy.money >= self.get_food_cost()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            if not agent.position.at_shop():  # Simplified because travel is implicit
                print("The agent moved to the shop")
                SysPosition.move_to_shop(agent.position)
            SysFood.add_food(agent.food, self.amount_beef, self.amount_chicken, self.amount_tofu)
            agent.economy.money -= self.get_food_cost()
            print("Buy food: B:" + str(self.amount_beef) + ", C:" + str(self.amount_chicken) + ", T:" + str(
                self.amount_tofu))
            agent.deliberation.actions_list.append(self.to_string())
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
            agent.deliberation.actions_list.append(self.to_string())
            return True
        else:
            print("ERROR")
            return False


class ActFootballGoalie(Action):

    def check_preconditions(self, agent: Human) -> bool:

        return True

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            print("The agent football as a goalie")
            agent.deliberation.actions_list.append(self.to_string())
            return True
        else:
            print("ERROR")
            return False


class ActFootballTeamplayer(Action):

    def check_preconditions(self, agent: Human) -> bool:

        return True

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            print("The agent played football as a team player")
            agent.deliberation.actions_list.append(self.to_string())
            return True
        else:
            print("ERROR")
            return False


class ActFootballSeriousPlayer(Action):

    def check_preconditions(self, agent: Human) -> bool:

        return True

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            print("The agent played football very seriously")
            agent.deliberation.actions_list.append(self.to_string())
            return True
        else:
            print("ERROR")
            return False
