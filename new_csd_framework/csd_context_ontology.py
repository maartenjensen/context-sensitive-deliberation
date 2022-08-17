from enum import Enum

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