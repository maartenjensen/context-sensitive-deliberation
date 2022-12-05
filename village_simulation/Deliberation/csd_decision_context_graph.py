import networkx as nx
from networkx import Graph

from village_simulation.Deliberation.csd_actions import Action, ActNone
from village_simulation.EComponentsS.enums import Activity


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

    def has_more_than_one_of_type(self, node_type):
        all_nodes = self.my_dc.nodes
        nodes_of_type = []
        for node in all_nodes:
            if isinstance(node, node_type):
                nodes_of_type.append(node)
        return len(nodes_of_type) > 1

    def has_more_than_one_activities(self):
        all_nodes = self.my_dc.nodes
        activities = []
        for node in all_nodes:
            if isinstance(node, Activity):
                activities.append(node)
        return len(activities) > 1

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

    def get_related_actions(self, node) -> []:
        neighbors = self.my_dc.adj[node]
        actions = []
        for node in neighbors:
            if isinstance(node, Action):
                actions.append(node)
        return actions

    def get_all_nodes_of_type(self, node_type):
        nodes_of_type = []
        for node in self.my_dc.nodes:
            if isinstance(node, node_type):
                nodes_of_type.append(node)
        return nodes_of_type

    def deactivate_other_activities_and_related(self, activity_to_stay: Activity):
        # activity_to_stay
        to_remove_activities = self.get_all_nodes_of_type(Activity)
        to_remove_activities.remove(activity_to_stay)

        # Check which nodes are connected to this activity but not to any other activity.
        to_remove_nodes = []
        for node in self.my_dc.nodes:
            if not isinstance(node, Activity):
                related_activities = self.get_related_activities(node)
                if activity_to_stay not in related_activities:
                    to_remove_nodes.append(node)

        for node in to_remove_nodes:
            self.my_dc.remove_node(node)

        for activity in to_remove_activities:
            self.my_dc.remove_node(activity)

    def is_empty(self) -> bool:
        all_nodes = self.my_dc.nodes
        if len(all_nodes) > 0:
            return False
        return True

    def get_dc_graph(self) -> Graph:
        return self.my_dc

    def print_all(self):
        print_string = "DC Nodes: "
        for node in self.my_dc.nodes:
            print_string += self.to_string_node(node) + ", "

        print(print_string)
        print_edges = "DC Edges: "
        for edge in self.my_dc.edges:
            node1_str = self.to_string_node(edge[0])
            node2_str = self.to_string_node(edge[1])
            print_edges += "[" + node1_str + "-" + node2_str + "], "

        print(print_edges)

    def to_string_node(self, node) -> str:

        if isinstance(node, NodeUrgency):
            return node.to_string()
        elif isinstance(node, NodeUtility):
            return node.to_string()
        elif isinstance(node, Action):
            return node.to_string()
        else:
            return str(node)


class NodeUrgency:

    def __init__(self, urgency_amount: float):
        self.urgency_amount = urgency_amount

    def get_urgency_amount(self) -> float:
        return self.urgency_amount

    def to_string(self) -> str:
        return "Urgency:" + "{:.2f}".format(self.urgency_amount)


class NodeUtility:

    def __init__(self, utility_amount: float):
        self.utility_amount = utility_amount

    def get_amount(self) -> float:
        return self.utility_amount

    def to_string(self) -> str:
        return "Utility:" + "{:.2f}".format(self.utility_amount)