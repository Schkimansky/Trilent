from enum import Enum
from Trilent.Window import Window


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'


class Widget:
    def __init__(self,
                 parent: Window,
                 width: int,
                 height: int,
                 positioning: str = 'auto'):
        if positioning == 'auto':
            positioning = parent._positionType
