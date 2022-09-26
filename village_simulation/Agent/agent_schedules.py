from village_simulation.Agent.enums import Activity, Days, DefaultFood

class ActivityInformation:

    def __init__(self, activity, travel_to, food_to_eat):
        self.activity = activity
        self.travel_to = travel_to
        self.food_to_eat = food_to_eat

class ScheduleTime:
    """ This schedule is based on time, most times will trigger specific activities """
    """ Maybe these dictionaries have to be replaced by for example a dataframe, numpy stuff??"""

    def __init__(self):
        self.time_schedule_mo = {}  # 0
        self.time_schedule_tu = {}
        self.time_schedule_we = {}
        self.time_schedule_th = {}
        self.time_schedule_fr = {}
        self.time_schedule_sa = {}
        self.time_schedule_su = {}

    def print_schedule(self):
        print(self.time_schedule_mo)
        print(self.time_schedule_sa)

    def get_activity_based_on_time(self, time: int, day: Days):
        time_based_activity = Activity.NONE
        if day == Days.MO:
            if time in self.time_schedule_mo:
                time_based_activity = self.time_schedule_mo[time]
        if day == Days.TU:
            if time in self.time_schedule_tu:
                time_based_activity = self.time_schedule_tu[time]
        if day == Days.WE:
            if time in self.time_schedule_we:
                time_based_activity = self.time_schedule_we[time]
        if day == Days.TH:
            if time in self.time_schedule_th:
                time_based_activity = self.time_schedule_th[time]
        if day == Days.FR:
            if time in self.time_schedule_fr:
                time_based_activity = self.time_schedule_fr[time]
        if day == Days.SA:
            if time in self.time_schedule_sa:
                time_based_activity = self.time_schedule_sa[time]
        if day == Days.SU:
            if time in self.time_schedule_su:
                time_based_activity = self.time_schedule_su[time]

        return time_based_activity

    def init_schedule_default_worker(self, default_food: DefaultFood):
        eating_activity = Activity.EAT
        if default_food == DefaultFood.BEEF:
            eating_activity = Activity.EAT_BEEF
        elif default_food == DefaultFood.CHICKEN:
            eating_activity = Activity.EAT_CHICKEN
        elif default_food == DefaultFood.TOFU:
            eating_activity = Activity.EAT_TOFU

        new_time_schedule_day = {0: Activity.SLEEP, 1: Activity.SLEEP, 2: Activity.SLEEP, 3: Activity.SLEEP,
                                 4: Activity.SLEEP, 5: Activity.SLEEP, 6: eating_activity, 12: eating_activity,
                                 18: Activity.EAT, 22: Activity.SLEEP, 23: Activity.SLEEP}

        self.time_schedule_mo.update(new_time_schedule_day)
        self.time_schedule_tu.update(new_time_schedule_day)
        self.time_schedule_we.update(new_time_schedule_day)
        self.time_schedule_th.update(new_time_schedule_day)
        self.time_schedule_fr.update(new_time_schedule_day)
        self.time_schedule_sa.update(new_time_schedule_day)
        self.time_schedule_su.update(new_time_schedule_day)

        new_time_schedule_work = {7: Activity.TRAVEL_TO_WORK, 8: Activity.WORK, 9: Activity.WORK, 10: Activity.WORK,
                                  11: Activity.WORK, 13: Activity.WORK, 14: Activity.WORK, 15: Activity.WORK,
                                  16: Activity.WORK, 17: Activity.TRAVEL_TO_HOME}

        self.time_schedule_mo.update(new_time_schedule_work)
        self.time_schedule_tu.update(new_time_schedule_work)
        self.time_schedule_we.update(new_time_schedule_work)
        self.time_schedule_th.update(new_time_schedule_work)
        self.time_schedule_fr.update(new_time_schedule_work)

        # Update the schedule with the new time schedule, here you could also add a check for conflicts, which
        # should let the agents deliberate more because it would be shitty to plan 2 activities at the same time.


class ScheduleLocation:
    """ This schedule is based on location, some locations will trigger specific activities """

    def __init__(self):
        self.loc_schedule = {}
