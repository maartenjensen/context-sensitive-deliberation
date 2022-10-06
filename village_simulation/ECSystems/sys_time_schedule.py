from village_simulation.EComponentsS.cmp_time_schedule import CmpTimeSchedule, ActivityInformation
from village_simulation.EComponentsS.enums import Activity, LocationEnum, DefaultFood

" The systems should become static "


class SysScheduleTime:
    """ This schedule is based on time, most times will trigger specific activities
        Maybe these dictionaries have to be replaced by for example a dataframe, numpy stuff??
        Simplified this timeschedule, now there are no weekends/weekdays, just one type of day,
        originally I implemented this and it could be useful for replanning but now I removed it """

    @staticmethod
    def set_time_schedule(time_schedule: CmpTimeSchedule):
        act_sleep = ActivityInformation(Activity.SLEEP)
        sleep_schedule = {0: act_sleep, 1: act_sleep, 2: act_sleep, 3: act_sleep,
                          4: act_sleep, 5: act_sleep, 23: act_sleep}

        act_eat = ActivityInformation(Activity.EAT)
        eating_schedule = {6: act_eat, 12: act_eat, 18: act_eat}

        act_work = ActivityInformation(Activity.WORK)
        working_schedule = {8: act_work, 9: act_work, 10: act_work, 11: act_work,
                            13: act_work, 14: act_work, 15: act_work, 16: act_work}

        travel_schedule = {7: ActivityInformation(Activity.TRAVEL, travel_to=LocationEnum.WORK),
                           17: ActivityInformation(Activity.TRAVEL, travel_to=LocationEnum.HOME)}

        shop_schedule = {19: ActivityInformation(Activity.TRAVEL, travel_to=LocationEnum.SHOP),
                         20: ActivityInformation(Activity.BUY_FOOD),
                         21: ActivityInformation(Activity.TRAVEL, travel_to=LocationEnum.HOME)}

        time_schedule.my_schedule.update(sleep_schedule)
        time_schedule.my_schedule.update(eating_schedule)
        time_schedule.my_schedule.update(working_schedule)
        time_schedule.my_schedule.update(travel_schedule)
        time_schedule.my_schedule.update(shop_schedule)

    @staticmethod
    def specify_food_in_schedule(time_schedule: CmpTimeSchedule, default_food: DefaultFood):
        act_eat = ActivityInformation(Activity.EAT, food_to_eat=default_food)
        specified_food_schedule = {6: act_eat, 12: act_eat, 18: act_eat}
        time_schedule.my_schedule.update(specified_food_schedule)

    @staticmethod
    def specify_buy_in_schedule(time_schedule: CmpTimeSchedule, beef_to_buy: int, chicken_to_buy: int,
                                tofu_to_buy: int):
        act_buy = ActivityInformation(Activity.BUY_FOOD, beef_to_buy=beef_to_buy,
                                      chicken_to_buy=chicken_to_buy, tofu_to_buy=tofu_to_buy)
        specified_food_schedule = {20: act_buy}
        time_schedule.my_schedule.update(specified_food_schedule)

    """ Specific functions """

    @staticmethod
    def custom_overwrite_buy_food(time_schedule: CmpTimeSchedule):
        specified_food_schedule = {20: ActivityInformation(Activity.BUY_FOOD)}
        time_schedule.my_schedule.update(specified_food_schedule)

    @staticmethod
    def custom_overwrite_buy_car(time_schedule: CmpTimeSchedule):
        specified_car_schedule = {22: ActivityInformation(Activity.BUY_CAR)}
        time_schedule.my_schedule.update(specified_car_schedule)

    @staticmethod
    def custom_overwrite_bought_a_car(time_schedule: CmpTimeSchedule):
        specified_leisure_schedule = {22: ActivityInformation(Activity.LEISURE)}
        time_schedule.my_schedule.update(specified_leisure_schedule)

    @staticmethod
    def custom_overwrite_eat_with_friend(time_schedule: CmpTimeSchedule, friend_id):
        specified_eating_schedule = {17: ActivityInformation(Activity.TRAVEL, travel_to=LocationEnum.SHOP),
                                     18: ActivityInformation(Activity.BUY_FOOD, eat_with_friend_id=friend_id),
                                     19: ActivityInformation(Activity.TRAVEL, eat_with_friend_id=friend_id),
                                     20: ActivityInformation(Activity.EAT_TOGETHER, eat_with_friend_id=friend_id),
                                     21: ActivityInformation(Activity.LEISURE, eat_with_friend_id=friend_id),
                                     22: ActivityInformation(Activity.TRAVEL, eat_with_friend_id=friend_id)}
        time_schedule.my_schedule.update(specified_eating_schedule)
