from enum import Enum


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'


class Widget:
    def __init__(self,
                 parent,
                 width: int,
                 height: int,
                 positioning: str = 'auto'):
        if positioning == 'auto':
            positioning = self._determine_position_type(parent)

    def _determine_position_type(self, parent) -> PositionTypes:
        if parent._positionType == PositionTypes.PLACE:
            print('absolute place')
