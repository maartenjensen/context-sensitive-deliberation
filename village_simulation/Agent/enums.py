from enum import Enum

class Activity(Enum):
    NONE = -1
    MORNING_ROUTINE = 0
    WORK = 1
    GET_FOOD = 2
    RELAXING = 3
    EAT = 4
    LEISURE = 5
    SLEEP = 6

class Need(Enum):
    NONE = -1
    HUNGER = 0
    FOOD = -1

class Plan(Enum): # Maybe this needs to contain explicit steps for the plan
    NONE = -1
    GET_FOOD = 0

class Goal(Enum):
    NONE = -1
    GET_FOOD = 0