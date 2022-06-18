# My imports
from csd_framework.csd_deliberator import *


class Agent:

    def __init__(self):
        print("Initialized:" + type(self).__name__)
        self.myDeliberator = Deliberator()

    def deliberate(self):
        self.myDeliberator.main_deliberate()
