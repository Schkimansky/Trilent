from PyQt5.QtWidgets import QFrame
from Trilent.Utility import get_in_pixels, get_as_qt
from Trilent.Widgets import PositionTypes


class Box:
    def __init__(self,
                 parent,
                 # Utility
                 width: int | str = '8 inch',
                 height: int | str = '5 inch',
                 x: int | str = '4 inch',
                 y: int | str = '3 inch',
                 # Color
                 background_color='#272727'):

        self._parent = parent
        self._positionType = PositionTypes.BOX
        self._dpi = parent.get_dpi()
        self._widgets = []

        self._frame = QFrame(parent._get_holder())

        # Setup properties
        self._frame.setStyleSheet(f"background-color: {get_as_qt(background_color)};")
        self._frame.setGeometry(get_in_pixels(x, self._dpi), get_in_pixels(y, self._dpi),
                                get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

        # Parent is also a box
        if self._parent._positionType == PositionTypes.BOX:
            self._parent._widget_box_add(self)

    def place(self, x: int = 100, y: int = 100):
        assert self._parent._positionType != PositionTypes.BOX, TypeError("You cant place a box whose parent is also a box.")

        geometry = self._frame.geometry()
        self._frame.setGeometry(x, y, geometry.width(), geometry.height())
        self._frame.show()

    def get_dpi(self): return self._parent.get_dpi()

    def _widget_box_add(self, trilent_widget):
        print('New widget added to box')
        print(trilent_widget)

        trilent_widget._box_signal_show()
        trilent_widget._box_signal_update_position(0, 0)

    def _get_holder(self): return self._frame

    def _box_signal_show(self):
        self._frame.show()

    def _box_signal_update_position(self, x, y):
        geometry = self._frame.geometry()
        self._frame.setGeometry(x, y, geometry.width(), geometry.height())
        print('widget box was placed!')
