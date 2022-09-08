from village_simulation.Agent.agents_parent import ParentAgent
from village_simulation.Model.model_parent import ParentModel


class Actions:

    def none_action(self, agent: ParentAgent, model: ParentModel):
        print("ERROR none_action should not be called")

    def just_chill(self, agent: ParentAgent, model: ParentModel):
        print("The agent has nothing to do and just chills")

    def sleep(self, agent: ParentAgent, model: ParentModel):
        print("Action: sleeping")

    def work(self, agent: ParentAgent, model: ParentModel):
        print("Action: work")

    def eat_beef(self, agent: ParentAgent, model: ParentModel):
        if agent.beef > 0:
            agent.beef -= 1
            print("eating beef")
        else:
            print("ERROR")

    def eat_chicken(self, agent: ParentAgent, model: ParentModel):
        if agent.chicken > 0:
            agent.chicken -= 1
            print("eating chicken")
        else:
            print("ERROR")

    def eat_tofu(self, agent: ParentAgent, model: ParentModel):
        if agent.tofu > 0:
            agent.tofu -= 1
            print("eating tofu")
        else:
            print("ERROR")
