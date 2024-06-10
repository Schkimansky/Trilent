from PyQt5.QtWidgets import QPushButton
from Trilent.Window import Window
from enum import Enum


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'


class Widget:
    def __init__(self,
                 parent: Window,
                 width: int,
                 height: int,
                 positioning: str = 'auto'):
        pass
