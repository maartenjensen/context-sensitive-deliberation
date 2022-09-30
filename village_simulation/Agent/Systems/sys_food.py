from village_simulation.Agent.Data.data_food import AgentFood


class SysAgentFood:

    def get_total_food(self, food: AgentFood):
        return food.beef + food.chicken + food.tofu

    def add_food(self, food: AgentFood, amount_beef, amount_chicken, amount_tofu):
        food.beef += amount_beef
        food.chicken += amount_chicken
        food.tofu += amount_tofu
