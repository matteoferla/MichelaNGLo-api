from enum import Enum

class Privacy(Enum):
    private = 0
    public = 1
    published = 2
    sgc = 3
    pinned = 4


class Location(Enum):
    left = 0
    right = 1