from village_simulation.EntitiesCS.the_agent import Human


class Action:

    def __init__(self, steps_active=0):
        self.steps_active = steps_active

    def check_preconditions(self, agent: Human) -> bool:
        print("Preconditions checked and accepted")
        return True

    def execute_action(self, agent: Human) -> bool:
        print("Executed action")
        agent.deliberation.actions_list.append(self.to_string())
        return True

    def action_step(self, agent: Human):
        self.steps_active -= 1
        if self.steps_active == 0:
            self.execute_action(agent)

    def to_string(self) -> str:
        return self.__class__.__name__

    def compare(self, other_action):
        if isinstance(other_action, Action):
            return type(other_action) == type(self)
        return False
