from village_simulation.Agent.Data.data_food import AgentFood


class SysAgentFood:

    def get_total_food(self, food: AgentFood):
        return food.beef + food.chicken + food.tofu
