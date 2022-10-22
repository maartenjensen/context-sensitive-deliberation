from village_simulation.EComponentsS.cmp_economy import CmpEconomy
from village_simulation.EComponentsS.cmp_food import CmpFood
from village_simulation.EComponentsS.cmp_needs import CmpNeeds


class SysNeeds:

    @staticmethod
    def update_needs(needs: CmpNeeds, economy: CmpEconomy, food: CmpFood, time: float, times_per_day: int):

        if time == 0:
            economy.worked_hours_day = 0

        # time is still a value from 0 to 24
        if time < 6 or time > 22:
            needs.sleep += 0.5

        if 7 <= time < 18 and economy.worked_hours_day < 8:
            needs.work = 0.9
        else:
            needs.work = 0

        if 6 <= time < 18:
            needs.hunger = min(2, needs.hunger + (1 / times_per_day * 4))  # in 6 hours the agent should be hungry
        else:
            needs.hunger = min(2, needs.hunger + (1 / times_per_day * 2))  # in 12 hours the agent should be hungry

        if food.get_total_food() < 6:
            needs.food_safety = (6.0 - food.get_total_food()) / 3
        else:
            needs.food_safety = 0

        needs.leisure = 0.4
