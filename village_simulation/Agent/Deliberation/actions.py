from village_simulation.Agent.agents import Human


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
        return True

    def execute_action(self, agent: Human) -> bool:
        print("The agent just chilled")
        return True


class ActSleep(Actions):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at home (simplification)")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("The agent slept")
        return True


class ActWork(Actions):

    def check_preconditions(self, agent: Human) -> bool:
        print("Check whether the agent is at work")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("The agent worked")
        return True


class ActEatBeef(Actions):

    def check_preconditions(self, agent: Human) -> bool:

        print("Check whether the agent has beef")
        return True

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

        print("Check whether the agent has beef")
        return True

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

        print("Check whether the agent has beef")
        return True

    def execute_action(self, agent: Human) -> bool:

        if agent.food.tofu > 0:
            agent.food.tofu -= 1
            print("Eating tofu")
            return True
        else:
            print("ERROR")
            return False
