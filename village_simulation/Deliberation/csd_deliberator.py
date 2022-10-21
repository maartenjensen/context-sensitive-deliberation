from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Deliberation.actions import ActNone, ActSleep, ActEatBeef, ActEatChicken, ActEatTofu
from village_simulation.EComponentsS.enums import Activity, DcElement, Goal
from village_simulation.EntitiesCS.the_agent import Human
import numpy as np


class DecisionContext:

    def __init__(self):
        # Main dictionaries
        self.activities = {}
        self.goals = {}
        self.plans = {}
        self.actions = {}

        self.relations = np.array([[-1, DcElement.NONE, -1, DcElement.NONE]])

        self.unique_id = 0

    def add_activity(self, activity, linked_id=-1, dc_element=DcElement.NONE) -> int:
        self.activities[self.unique_id] = activity
        if linked_id >= 0:
            self.add_relation(self.unique_id, DcElement.ACTIVITY, linked_id, dc_element)
        return self.increase_unique_id()

    def add_goal(self, goal, linked_id=-1, dc_element=DcElement.NONE) -> int:
        self.goals[self.unique_id] = goal
        if linked_id >= 0:
            self.add_relation(self.unique_id, DcElement.ACTIVITY, linked_id, dc_element)
        return self.increase_unique_id()

    def add_plan(self, plan, linked_id=-1, dc_element=DcElement.NONE) -> int:
        self.plans[self.unique_id] = plan
        if linked_id >= 0:
            self.add_relation(self.unique_id, DcElement.ACTIVITY, linked_id, dc_element)
        return self.increase_unique_id()

    def add_action(self, actions, linked_id=-1, dc_element=DcElement.NONE) -> int:
        self.actions[self.unique_id] = actions
        if linked_id >= 0:
            self.add_relation(self.unique_id, DcElement.ACTIVITY, linked_id, dc_element)
        return self.increase_unique_id()

    def add_relation(self, id_1, type_1, id_2, type_2):
        added_relation = [[id_1, type_1, id_2, type_2]]
        self.relations = np.append(self.relations, added_relation, axis=0)
        # self.relations = np.delete(self.relations, [[-1, DcElement.NONE, -1, DcElement.NONE]], axis=0)

    def remove_activities_and_related_except(self, activity_id):

        to_remove_ids = []
        for key, value in self.activities.items():
            if activity_id != key:
                to_remove_ids.append(activity_id)
                self.remove_related(activity_id)

        for i in to_remove_ids:
            self.activities.pop(i)

    def remove_related(self, t_id):

        to_remove_indexes = []
        for i in range(len(self.relations) - 1):
            row = self.relations[i]
            if row[0] == t_id:
                self.remove_based_on_id(row[2])
                to_remove_indexes.append(i)
            elif row[2] == t_id:
                self.remove_based_on_id(row[0])
                to_remove_indexes.append(i)

        to_remove_indexes.reverse()
        for index in to_remove_indexes:
            np.delete(self.relations, index, 0)

    def remove_based_on_id(self, t_id):
        for key, value in self.activities.items():
            if key == t_id:
                self.activities.pop(t_id)
                return
        for key, value in self.goals.items():
            if key == t_id:
                self.goals.pop(t_id)
                return
        for key, value in self.plans.items():
            if key == t_id:
                self.plans.pop(t_id)
                return
        for key, value in self.actions.items():
            if key == t_id:
                self.actions.pop(t_id)
                return

    def get_object_from_id(self, t_id):
        for key, value in self.activities.items():
            if key == t_id:
                return value
        for key, value in self.goals.items():
            if key == t_id:
                return value
        for key, value in self.plans.items():
            if key == t_id:
                return value
        for key, value in self.actions.items():
            if key == t_id:
                return value
        return None

    def has_one_action(self) -> True:
        return len(self.actions.keys()) == 1

    def get_one_action_id(self) -> int:
        for key, value in self.actions.items():
            return key
        return None

    def get_one_action(self):
        for key, value in self.actions.items():
            return value
        return None

    def get_linked_activity(self, t_id):
        """ Retrieves a linked activity """
        activity_id = -1
        for row in self.relations:
            if row[0] == t_id and row[3] == DcElement.ACTIVITY:
                activity_id = row[2]
            elif row[2] == t_id and row[1] == DcElement.ACTIVITY:
                activity_id = row[0]
            if activity_id >= 0:
                return self.activities.get(activity_id)

    def get_linked_activity_id(self, t_id):
        """ Retrieves a linked activity """
        activity_id = -1
        for row in self.relations:
            if row[0] == t_id and row[3] == DcElement.ACTIVITY:
                activity_id = row[2]
            elif row[2] == t_id and row[1] == DcElement.ACTIVITY:
                activity_id = row[0]
            if activity_id >= 0:
                return activity_id

    def str_activity(self):
        string = ""
        for key, value in self.activities.items():
            string += str(key) + ":" + str(value) + ", "
        return string

    def str_goal(self):
        string = ""
        for key, value in self.goals.items():
            string += str(key) + ":" + str(value) + ", "
        return string

    def str_plan(self):
        string = ""
        for key, value in self.plans.items():
            string += str(key) + ":" + str(value) + ", "
        return string

    def str_action(self):
        string = ""
        for key, value in self.actions.items():
            string += str(key) + ":" + str(value) + ", "
        return string

    def str_relations(self):
        string = ""
        for row in self.relations:
            if row[0] != -1:
                string += str(row) + ", "
        return string

    def print_activity(self):
        print(self.str_activity())

    def print_action(self):
        print(self.str_action())

    def print_all(self):
        print(
            "Actv= " + self.str_activity() + "Goal= " + self.str_goal() + "Plan= " + self.str_plan() + "Action= " + self.str_action())
        print("Relations= " + self.str_relations())

    def increase_unique_id(self) -> int:
        self.unique_id += 1
        return self.unique_id - 1


class DecisionContextExt(DecisionContext):

    def __init__(self):
        super().__init__()

        # Other dictionaries
        self.urgency = {}

    def add_urgency(self, urgency, linked_id=-1, dc_element=DcElement.NONE) -> int:
        self.urgency[self.unique_id] = urgency
        if linked_id >= 0:
            self.add_relation(self.unique_id, DcElement.ACTIVITY, linked_id, dc_element)
        return self.increase_unique_id()

    def get_object_from_id(self, t_id):
        dc_object = super().get_object_from_id(t_id)
        if dc_object is not None:
            return dc_object

        for key, value in self.urgency.items():
            if key == t_id:
                return value
        return None

    def remove_based_on_id(self, t_id):
        """ TODO let this functions return true/false, True when the id has been removed """
        super().remove_based_on_id(t_id)

        for key, value in self.urgency.items():
            if key == t_id:
                self.urgency.pop(t_id)
        return

    def str_urgency(self):
        string = ""
        for key, value in self.urgency.items():
            string += str(key) + ":" + str(value) + ", "
        return string

    def print_urgency(self):
        print(self.str_urgency())

    def print_all(self):
        super().print_all()
        print("Urgency:" + self.str_urgency())


class Deliberator:

    def __init__(self):
        self.actNone = ActNone()
        self.actSleep = ActSleep()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()

        self.dc = DecisionContextExt()
        print("Initialize deliberator")

    def deliberate(self, agent: Human):

        print("Start deliberation")
        self.dc = DecisionContextExt()
        chosen_action = self.actNone
        chosen_activity = Activity.NONE

        print("Get habits from time")
        self.set_typical_habit_from_time()
        self.dc.print_all()

        # Perform action
        if self.dc.has_one_action():
            action_id = self.dc.get_one_action_id()
            chosen_action = self.dc.get_object_from_id(action_id)
            chosen_activity = self.dc.get_linked_activity(action_id)

            if self.check_and_execute_action(agent, chosen_action):
                self.save_agent_activity(agent, chosen_activity)
                return

        self.set_urgency_of_activities(agent)
        most_urgent_activity_id = self.get_most_urgent_activity_id()
        if most_urgent_activity_id >= 0:
            self.dc.remove_activities_and_related_except(most_urgent_activity_id)

        self.dc.print_all()

        # Perform action
        if self.dc.has_one_action():
            action_id = self.dc.get_one_action_id()
            chosen_action = self.dc.get_object_from_id(action_id)
            chosen_activity = self.dc.get_linked_activity(action_id)

            if self.check_and_execute_action(agent, chosen_action):
                self.save_agent_activity(agent, chosen_activity)
                return

        print("More deliberation is needed")

    def set_typical_habit_from_time(self):

        # TODO include working day
        # Agents could have certain anchor points, e.g. an agent likes to start working at

        time = SimUtils.get_model().get_time_day()
        if 0 <= time <= 8 or time >= 22:
            self.add_habit_sleeping()
        if 5 <= time <= 8 or 11 <= time <= 14 or 17 <= time <= 20:
            self.add_habit_eat()
        # if 7 <= time <= 18:
        #     self.set_habit_work()
        # if 18 <= time <= 20:
        #     self.set_habit_buy_food()
        # if 18 <= time <= 23:
        #     self.set_habit_leisure()
        # return activities

    def set_urgency_of_activities(self, agent: Human):

        for key, value in self.dc.activities.items():
            if value == Activity.SLEEP:
                self.dc.add_urgency(agent.needs.sleep, key, DcElement.ACTIVITY)
            elif value == Activity.EAT:
                self.dc.add_urgency(agent.needs.hunger, key, DcElement.ACTIVITY)

    def get_most_urgent_activity_id(self) -> int:

        highest = -1.0
        highest_id = -1
        for key, value in self.dc.urgency.items():
            if value > highest or highest_id == -1:
                highest = value
                highest_id = key

        return self.dc.get_linked_activity_id(highest_id)


    def add_habit_sleeping(self):

        id_activity = self.dc.add_activity(Activity.SLEEP)
        self.dc.add_action(self.actSleep, id_activity, DcElement.ACTIVITY)

    def add_habit_eat(self):

        id_activity = self.dc.add_activity(Activity.EAT)
        id_goal = self.dc.add_activity(Goal.EAT_FOOD, id_activity, DcElement.ACTIVITY)
        self.dc.add_action(self.actEatChicken, id_goal, DcElement.GOAL)

    # def set_habit_work(self):

    # def set_habit_buy_food(self):

    # def set_habit_leisure(self):

    def check_and_execute_action(self, agent: Human, action) -> bool:

        if action != self.actNone:
            if action.check_preconditions(agent):
                action.execute_action(agent)
                agent.deliberation.current_action = action
                return True

        return False

    def save_agent_activity(self, agent: Human, activity: Activity):
        agent.deliberation.current_activity = activity
