from village_simulation.DelibFramework.csd_decision_context_graph import DecisionContext
from village_simulation.DelibCustom.csd_decision_context_nodes_custom import NodeUrgency
from village_simulation.EComponentsS.simulation_enums import Activity, Criteria
from village_simulation.EntitiesCS.the_agent import Human

# Maybe this has to be a static class
class TupleNarrowing:

    def __init__(self):
        print("Init tuple narrowing")

        self.narrow_activities = {}
        self.narrow_goals = []
        self.narrow_plans = []
        self.narrow_actions = []

    # ===========================================
    #   Narrow down
    # ===========================================
    def narrow_based_on_criteria(self, dc: DecisionContext, agent: Human, criteria: Criteria):

        print("Narrow based on criteria")
        if criteria == criteria.URGENCY:
            self.set_urgency_of_activities(dc, agent)

            most_urgent_activities = self.get_most_urgent_activities(dc)
            if len(most_urgent_activities) == 1:
                most_urgent_activity = most_urgent_activities[0]
                dc.deactivate_other_activities_and_related(most_urgent_activity)

    def get_most_urgent_activities(self, dc: DecisionContext) -> []:

        highest = -1.0
        highest_object = None
        for urgency_node in dc.get_all_nodes_of_type(NodeUrgency):
            if isinstance(urgency_node, NodeUrgency):
                if urgency_node.get_urgency_amount() > highest or highest_object is None:
                    highest = urgency_node.get_urgency_amount()
                    highest_object = urgency_node

        if highest_object is None:
            return []
        else:
            return dc.get_related_activities(highest_object)

    def set_urgency_of_activities(self, dc: DecisionContext, agent: Human):

        for activity_node in dc.get_all_nodes_of_type(Activity):
            if activity_node == Activity.SLEEP:
                dc.add_node_and_edge(NodeUrgency(agent.needs.sleep), activity_node)
            elif activity_node == Activity.EAT:
                dc.add_node_and_edge(NodeUrgency(agent.needs.hunger), activity_node)
            elif activity_node == Activity.WORK:
                dc.add_node_and_edge(NodeUrgency(agent.needs.work), activity_node)
            elif activity_node == Activity.BUY_FOOD:
                dc.add_node_and_edge(NodeUrgency(agent.needs.food_safety), activity_node)
            elif activity_node == Activity.LEISURE:
                dc.add_node_and_edge(NodeUrgency(agent.needs.leisure), activity_node)
            elif activity_node == Activity.FOOTBALL:
                dc.add_node_and_edge(NodeUrgency(2),
                                     activity_node)  # Hardcoded high value since football is planned