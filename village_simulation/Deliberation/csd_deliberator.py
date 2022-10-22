from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Deliberation.actions import ActNone, ActSleep, ActEatBeef, ActEatChicken, ActEatTofu, Action
from village_simulation.EComponentsS.enums import Activity, DcElement, Goal
from village_simulation.EntitiesCS.the_agent import Human
import numpy as np
import networkx as nx

# https://groups.google.com/g/networkx-discuss/c/dZfKl6u7P5A?hl=en&pli=1
# networkx for graph structure


class Urgency:

    def __init__(self, urgency_amount: float):
        self.urgency_amount = urgency_amount

    def get_urgency_amount(self) -> float:
        return self.urgency_amount


class DecisionContext:

    def __init__(self):
        # Main dictionaries
        self.my_dc = nx.Graph()

    def add_node(self, node_obj):
        self.my_dc.add_node(node_obj)

    def add_node_and_edge(self, node_obj, node_obj_2):
        self.my_dc.add_node(node_obj)
        self.my_dc.add_edge(node_obj, node_obj_2)

    def add_edge(self, node_obj_1, node_obj_2):
        self.my_dc.add_edge(node_obj_1, node_obj_2)

    def has_one_action(self):
        all_nodes = self.my_dc.nodes
        actions = []
        for node in all_nodes:
            if isinstance(node, Action):
                actions.append(node)
        return len(actions) == 1

    def get_one_action_if_one(self):
        all_nodes = self.my_dc.nodes
        actions = []
        for node in all_nodes:
            if isinstance(node, Action):
                actions.append(node)
        if len(actions) == 1:
            return actions[0]
        else:
            return ActNone()

    def get_related_activities(self, node) -> []:
        neighbors = self.my_dc.adj[node]
        activities = []
        for node in neighbors:
            if isinstance(node, Activity):
                activities.append(node)
        return activities

    def get_all_nodes_of_type(self, node_type):
        nodes_of_type = []
        for node in self.my_dc.nodes:
            if isinstance(node, node_type):
                nodes_of_type.append(node)
        return nodes_of_type

    def deactivate_other_activities_and_related(self, activity_to_stay:Activity):
        # activity_to_stay
        print("Deactivate all")
        to_remove_activities = self.get_all_nodes_of_type(Activity)
        print(to_remove_activities)
        to_remove_activities.remove(activity_to_stay)
        print(to_remove_activities)

        # Check which nodes are connected to this activity but not to any other activity.
        to_remove_nodes = []
        for node in self.my_dc.nodes:
            if not isinstance(node, Activity):
                related_activities = self.get_related_activities(node)
                if activity_to_stay not in related_activities:
                    to_remove_nodes.append(node)
        print(to_remove_nodes)

        for node in to_remove_nodes:
            self.my_dc.remove_node(node)

        for activity in to_remove_activities:
            self.my_dc.remove_node(activity)


    def print_all(self):
        print("DC nodes:" + str(list(self.my_dc.nodes)))
        print("DC edges:" + str(list(self.my_dc.edges)))


class Deliberator:

    def __init__(self):
        self.actNone = ActNone()
        self.actSleep = ActSleep()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()

        self.dc = DecisionContext()
        print("Initialize deliberator")

    def deliberate(self, agent: Human):

        print("Start deliberation")
        self.dc = DecisionContext()
        chosen_action = self.actNone
        chosen_activity = Activity.NONE
        self.reset_agent_deliberation_cost(agent)

        """ Urgency check """
        print("Get habits from time")
        self.set_typical_habit_from_time()
        self.dc.print_all()
        self.increase_agent_deliberation_cost(agent, 1)

        # Perform action
        if self.dc.has_one_action():
            chosen_action = self.dc.get_one_action_if_one()
            related_activities = self.dc.get_related_activities(chosen_action)
            if len(related_activities) > 0:
                chosen_activity = self.dc.get_related_activities(chosen_action)

            if self.check_and_execute_action(agent, chosen_action):
                self.save_agent_activity(agent, chosen_activity)
                return

        """ Urgency check """
        print("Urgency check")
        self.set_urgency_of_activities(agent)
        self.dc.print_all()
        most_urgent_activities = self.get_most_urgent_activities()
        if len(most_urgent_activities) == 1:
            most_urgent_activity = most_urgent_activities[0]
            self.dc.deactivate_other_activities_and_related(most_urgent_activity)
        self.increase_agent_deliberation_cost(agent, 1)

        # Perform action
        if self.dc.has_one_action():
            chosen_action = self.dc.get_one_action_if_one()
            related_activities = self.dc.get_related_activities(chosen_action)
            if len(related_activities) > 0:
                chosen_activity = self.dc.get_related_activities(chosen_action)

            if self.check_and_execute_action(agent, chosen_action):
                self.save_agent_activity(agent, chosen_activity)
                return

        self.dc.print_all()

        print("Something else")
        self.increase_agent_deliberation_cost(agent, 1)
        # self.increase_agent_deliberation_cost(agent, 1)
        # # Perform action
        # if self.dc.has_one_action():
        #     action_id = self.dc.get_one_action_id()
        #     chosen_action = self.dc.get_object_from_id(action_id)
        #     chosen_activity = self.dc.get_related_activities(action_id)
        #
        #     if self.check_and_execute_action(agent, chosen_action):
        #         self.save_agent_activity(agent, chosen_activity)
        #         return


        print("More deliberation is needed")

    def reset_agent_deliberation_cost(self, agent: Human):
        agent.deliberation.delib_cost = 0

    def increase_agent_deliberation_cost(self, agent: Human, deliberation_cost: int):
        agent.deliberation.delib_cost += deliberation_cost

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

        for activity_node in self.dc.get_all_nodes_of_type(Activity):
            if activity_node == Activity.SLEEP:
                self.dc.add_node_and_edge(Urgency(agent.needs.sleep), activity_node)
            elif activity_node == Activity.EAT:
                self.dc.add_node_and_edge(Urgency(agent.needs.hunger), activity_node)

    def get_most_urgent_activities(self) -> []:

        highest = -1.0
        highest_object = None
        for urgency_node in self.dc.get_all_nodes_of_type(Urgency):
            if isinstance(urgency_node, Urgency):
                if urgency_node.get_urgency_amount() > highest or highest_object is None:
                    highest = urgency_node.get_urgency_amount()
                    highest_object = urgency_node

        if highest_object is None:
            return []
        else:
            return self.dc.get_related_activities(highest_object)

    def add_habit_sleeping(self):

        self.dc.add_node(Activity.SLEEP)
        self.dc.add_node_and_edge(self.actSleep, Activity.SLEEP)

    def add_habit_eat(self):

        self.dc.add_node(Activity.EAT)
        self.dc.add_node_and_edge(Goal.EAT_FOOD, Activity.EAT)
        self.dc.add_node_and_edge(self.actEatChicken, Activity.EAT)
        self.dc.add_edge(self.actEatChicken, Goal.EAT_FOOD)

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
