from village_simulation.Agent.Data.enums import LocationEnum, Activity, DefaultFood


class ActivityInformation:

    def __init__(self, activity, *, travel_to=LocationEnum.NONE, food_to_eat=DefaultFood.NONE,
                 beef_to_buy=0, chicken_to_buy=0, tofu_to_buy=0, car_to_buy=0):
        self.activity = activity
        self.travel_to = travel_to
        self.food_to_eat = food_to_eat
        self.beef_to_buy = beef_to_buy
        self.chicken_to_buy = chicken_to_buy
        self.tofu_to_buy = tofu_to_buy
        self.car_to_buy = car_to_buy


class TimeSchedule:

    def __init__(self):
        leisure_time = ActivityInformation(Activity.LEISURE)
        self.my_schedule = {0: leisure_time, 1: leisure_time, 2: leisure_time, 3: leisure_time, 4: leisure_time,
                            5: leisure_time, 6: leisure_time, 7: leisure_time, 8: leisure_time, 9: leisure_time,
                            10: leisure_time, 11: leisure_time, 12: leisure_time, 13: leisure_time, 14: leisure_time,
                            15: leisure_time, 16: leisure_time, 17: leisure_time, 18: leisure_time, 19: leisure_time,
                            20: leisure_time, 21: leisure_time, 22: leisure_time, 23: leisure_time}

    def get_activity_based_on_time(self, time: int) -> ActivityInformation:
        return self.my_schedule[time]

    def print_schedule(self):
        schedule_str = ""
        for time, activity_inf in self.my_schedule.items():
            schedule_str += str(time) + '->' + str(activity_inf.activity)
            if activity_inf.activity == Activity.TRAVEL:
                schedule_str += " " + str(activity_inf.travel_to)
            elif activity_inf.activity == Activity.EAT:
                schedule_str += " " + str(activity_inf.food_to_eat)
            elif activity_inf.activity == Activity.BUY_FOOD:
                schedule_str += " B:" + str(activity_inf.beef_to_buy) + " C:" + str(activity_inf.chicken_to_buy)
                schedule_str += " T:" + str(activity_inf.tofu_to_buy)

            schedule_str += ", "

        print(schedule_str)
