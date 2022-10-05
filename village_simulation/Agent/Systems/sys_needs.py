import math

from village_simulation.Agent.Data.data_needs import AgentDataNeeds


class SysNeeds:

    @staticmethod
    def update_needs(needs: AgentDataNeeds, time: int, times_per_day: int):

        # time is still a value from 0 to 24
        if 6 <= time < 23:
            needs.sleep = 0
        else:
            needs.sleep = 1

        if 8 <= time < 12 or 13 <= time < 17:
            needs.work = 1
        else:
            needs.work = 0

        if 6 <= time < 18:
            needs.hunger = min(2, needs.hunger + (1/times_per_day * 4))  # in 6 hours the agent should be hungry
        else:
            needs.hunger = min(2, needs.hunger + (1/times_per_day * 2))  # in 12 hours the agent should be hungry
