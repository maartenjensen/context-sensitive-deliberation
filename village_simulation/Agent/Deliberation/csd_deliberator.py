from village_simulation.Agent.Deliberation.new_csd_context_module import ContextTimeActivity
from village_simulation.Agent.Deliberation.actions import ActSleep, ActWork, ActChill, ActEatBeef, ActEatChicken, \
    ActEatTofu, \
    ActNone, Actions, ActTravelToHome, ActTravelToWork, ActTravelToShop
from village_simulation.Agent.agents import Human
from village_simulation.Agent.enums import Activity, Urgency, Origin

""" The deliberator class contains all the deliberation functions, it explores the context and calls
    the deliberation functions to help with decision making """


class Deliberator:

    def __init__(self):
        print("Initialize Context modules")
        self.CTimeActivity = ContextTimeActivity()

        self.actNone = ActNone()
        self.actChill = ActChill()
        self.actSleep = ActSleep()
        self.actWork = ActWork()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()
        self.actTravelToHome = ActTravelToHome()
        self.actTravelToWork = ActTravelToWork()
        self.actTravelToShop = ActTravelToShop()

    def deliberate(self, agent: Human):

        self.CTimeActivity.explore_context(agent)
        self.CTimeActivity.print_context()

        action_object = self.get_action_from_activity(self.CTimeActivity.time_based_activity)
        action_object.check_preconditions(agent)
        if action_object != self.actNone:
            return action_object
        else:
            print("Good the program works, an actNone has been returned")
            return action_object

        # There can at some point also be multiple activities right?

    def get_action_from_activity(self, activity) -> Actions:

        if activity == Activity.SLEEP:
            return self.actSleep
        elif activity == Activity.WORK:
            return self.actWork
        elif activity == Activity.EAT:
            return self.actChill
        elif activity == Activity.EAT_BEEF:
            return self.actEatBeef
        elif activity == Activity.EAT_CHICKEN:
            return self.actEatChicken
        elif activity == Activity.EAT_TOFU:
            return self.actEatTofu
        elif activity == Activity.TRAVEL_TO_HOME:
            return self.actTravelToHome
        elif activity == Activity.TRAVEL_TO_SHOP:
            return self.actTravelToShop
        elif activity == Activity.TRAVEL_TO_WORK:
            return self.actTravelToWork

        return self.actNone


class ActivityHandler:

    def __init__(self):

        self.activities = [ActivityWrapper(Activity.NONE, Urgency.NONE, Origin.NONE)]
        self.activities.pop()

    def add_activity(self, activity: Activity, urgency: Urgency, origin: Origin):
        activity = ActivityWrapper(activity, urgency, origin)
        self.activities.append(activity)

    def remove_activity_by_origin(self, origin: Origin):
        temp_activities = [ActivityWrapper(Activity.NONE, Urgency.NONE, Origin.NONE)]
        temp_activities.pop()

        for act in self.activities:
            if act.origin != origin:
                temp_activities.append(act)

        self.activities = temp_activities


class ActivityWrapper:

    def __init__(self, activity: Activity, urgency: Urgency, origin: Origin):
        self.activity = activity
        self.urgency = urgency
        self.origin = origin
