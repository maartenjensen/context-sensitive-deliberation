from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Model.model_parent import ParentModel


class Actions:

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
