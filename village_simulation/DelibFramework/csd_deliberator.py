from village_simulation.DelibFramework.csd_decision_context_graph import DecisionContext

class Deliberator:

    def __init__(self):

        # Defined deliberation assist classes
        print("Initialize deliberator super class")
        #self.defAct = DefaultActionsContainer()
        self.dc = DecisionContext()

    # Create deliberate function
    # def deliberate(self):
    #    # deliberate main function
    #    print("Default deliberate function")
