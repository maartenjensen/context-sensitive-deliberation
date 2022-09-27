from village_simulation.Agent.Data.the_agent import Human


class Actions:

    def check_preconditions(self, agent: Human) -> bool:
        print("Preconditions checked and accepted")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("Executed action")
        return True


class ActNone(Actions):

    def check_preconditions(self, agent: Human) -> bool:
        print("Should not be called")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("This function should not even be called")
        return True


class ActChill(Actions):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return agent.position.at_home()

    def execute_action(self, agent: Human) -> bool:
        print("The agent just chilled")
        return True


class ActSleep(Actions):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return agent.position.at_home()

    def execute_action(self, agent: Human) -> bool:
        print("The agent slept")
        return True


class ActWork(Actions):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at work")
        return agent.position.at_work()

    def execute_action(self, agent: Human) -> bool:
        print("The agent worked")
        return True


class ActEatBeef(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has beef")
        return agent.food.beef > 0

    def execute_action(self, agent: Human) -> bool:

        if agent.food.beef > 0:
            agent.food.beef -= 1
            print("Eating beef")
            return True
        else:
            print("ERROR")
            return False


class ActEatChicken(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has chicken")
        return agent.food.chicken > 0

    def execute_action(self, agent: Human) -> bool:

        if agent.food.chicken > 0:
            agent.food.chicken -= 1
            print("Eating chicken")
            return True
        else:
            print("ERROR")
            return False


class ActEatTofu(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has tofu")
        return agent.food.tofu > 0

    def execute_action(self, agent: Human) -> bool:

        if agent.food.tofu > 0:
            agent.food.tofu -= 1
            print("Eating tofu")
            return True
        else:
            print("ERROR")
            return False


class ActTravelToWork(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is not already at work")
        return not agent.position.at_work()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            agent.position.move_to_office()
            print("Moving to office")
            return True
        else:
            print("ERROR")
            return False


class ActTravelToHome(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is not already at home")
        return not agent.position.at_home()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            agent.position.move_to_house()
            print("Moving to home")
            return True
        else:
            print("ERROR")
            return False


class ActTravelToShop(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent is not already at the shop")
        return not agent.position.at_shop()

    def execute_action(self, agent: Human) -> bool:

        if self.check_preconditions(agent):
            agent.position.move_to_shop()
            print("Moving to shop")
            return True
        else:
            print("ERROR")
            return False
