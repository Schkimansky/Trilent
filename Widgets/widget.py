from enum import Enum
from PyQt5.QtWidgets import QFrame
from Trilent.Utility import get_as_qt, get_in_pixels


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'


class Widget:
    def __init__(self,
                 parent,
                 width: int | str,
                 height: int | str,
                 excess_color: str = 'red'):

        self._window = QFrame(parent._get_holder())
        self._window.setGeometry(0,0, get_in_pixels(width, parent.get_dpi()), get_in_pixels(height, parent.get_dpi()))
        self._window.setStyleSheet(f"""background-color: {get_as_qt(excess_color)};""")

        self._positioning = parent._positionType
        if self._positioning == PositionTypes.BOX:
            parent._widget_box_add(self)
        print(self._positioning)

    def place(self, x: int = 100, y: int = 100):
        assert self._positioning != PositionTypes.BOX, TypeError("You cant place a widget whose parent is a box.")

        geometry = self._window.geometry()
        self._window.setGeometry(x, y, geometry.width(), geometry.height())
        self._window.show()

    def _box_signal_update_position(self, x, y):
        geometry = self._window.geometry()
        self._window.setGeometry(x, y, geometry.width(), geometry.height())

    def _get_holder(self):
        return self._window
