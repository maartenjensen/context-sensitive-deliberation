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
