from village_simulation.DelibFramework.csd_actions import Action
from village_simulation.DelibFramework.csd_decision_context_graph import DecisionContext
from village_simulation.DelibCustom.csd_decision_context_nodes_custom import NodeUrgency, NodeUtility


class DecisionContextCustom(DecisionContext):

    def __init__(self):
        # Main dictionaries
        super().__init__()

    def to_string_node(self, node) -> str:

        if isinstance(node, NodeUrgency):
            return node.to_string()
        elif isinstance(node, NodeUtility):
            return node.to_string()
        elif isinstance(node, Action):
            return node.to_string()
        else:
            return str(node)