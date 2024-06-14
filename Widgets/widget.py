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
                 excess_color: str = 'transparent'):

        self._frame = QFrame(parent._get_holder())
        self._frame.setGeometry(0, 0, get_in_pixels(width, parent.get_dpi()), get_in_pixels(height, parent.get_dpi()))
        self._frame.setStyleSheet(f"""background-color: {get_as_qt(excess_color)};""")

        self._positioning = parent._positionType
        if self._positioning == PositionTypes.BOX:
            parent._widget_box_add(self)

    def place(self, x: int = 100, y: int = 100):
        assert self._positioning != PositionTypes.BOX, TypeError("You cant place a widget whose parent is a box.")

        geometry = self._frame.geometry()
        self._frame.setGeometry(x, y, geometry.width(), geometry.height())
        self._frame.show()

    @property
    def width(self): return self._frame.width()
    @property
    def height(self): return self._frame.height()
    @property
    def x(self): return self._frame.x()
    @property
    def y(self): return self._frame.y()

    def show(self): self._frame.show()
    def hide(self): self._frame.hide()

    def set_position(self, x, y):
        geometry = self._frame.geometry()
        self._frame.setGeometry(x, y, geometry.width(), geometry.height())

    def _get_holder(self):
        return self._frame
