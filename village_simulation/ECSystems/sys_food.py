from village_simulation.EComponentsS.cmp_food import CmpFood


class SysFood:

    @staticmethod
    def get_total_food(food: CmpFood):
        return food.beef + food.chicken + food.tofu

    @staticmethod
    def add_food(food: CmpFood, amount_beef, amount_chicken, amount_tofu):
        food.beef += amount_beef
        food.chicken += amount_chicken
        food.tofu += amount_tofu
