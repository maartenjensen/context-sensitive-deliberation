from enum import Enum

""" I"m putting everything in an Enum because otherwise its just being a big mess if I put enums in multiple files """


class Activity(Enum):
    NONE = -1
    MORNING_ROUTINE = 0
    WORK = 1
    GET_FOOD = 2
    RELAXING = 3
    EAT = 4
    LEISURE = 5
    SLEEP = 6
    EAT_BEEF = 7
    EAT_CHICKEN = 8
    EAT_TOFU = 9


class Need(Enum):
    NONE = -1
    HUNGER = 0
    FOOD = -1


class Plan(Enum):  # Maybe this needs to contain explicit steps for the plan
    NONE = -1
    GET_FOOD = 0


class Goal(Enum):
    NONE = -1
    GET_FOOD = 0


class Location(Enum):
    NONE = -1
    HOME = 0
    HOUSE = 1
    OUTSIDE = 2
    SHOP = 3


class DefaultFood(Enum):
    NONE = -1
    BEEF = 0
    CHICKEN = 1
    TOFU = 2


class Days(Enum):
    NONE = -1
    MO = 1
    TU = 2
    WE = 3
    TH = 4
    FR = 5
    SA = 6
    SU = 7
