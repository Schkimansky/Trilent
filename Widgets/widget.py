from enum import Enum
from PyQt5.QtWidgets import QFrame
from Trilent.Utility import get_as_qt, get_in_pixels, PropertyManager


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'
    NONE: str = 'None specified.'


class Widget:
    def __init__(self,
                 parent,
                 width: int | str,
                 height: int | str,
                 excess_color: str = 'transparent'):

        # Properties setup
        self._properties = PropertyManager(parent=parent,
                                           excess_color=excess_color)

        self._position_self = self._properties['parent']._position_children
        self._position_children = PositionTypes.NONE

        self._widget_base_frame = QFrame(parent._get_holder())
        self._widget_base_frame.setGeometry(0, 0, get_in_pixels(width, parent.get_dpi()), get_in_pixels(height, parent.get_dpi()))
        self._widget_base_frame.setStyleSheet(f"""background-color: {get_as_qt(excess_color)};""")

        if self._properties['parent']._position_children == PositionTypes.BOX:
            parent._widget_box_add(self)

    def place(self, x: int = 100, y: int = 100):
        assert self._properties['parent']._position_self != PositionTypes.BOX, TypeError("You cant place a widget whose parent is a box.")

        geometry = self._widget_base_frame.geometry()
        self._widget_base_frame.setGeometry(x, y, geometry.width(), geometry.height())
        self._widget_base_frame.show()

    def force_place(self, x: int = 100, y: int = 100):
        geometry = self._widget_base_frame.geometry()
        self._widget_base_frame.setGeometry(x, y, geometry.width(), geometry.height())
        self._widget_base_frame.show()

    @property
    def width(self): return self._widget_base_frame.width()
    @property
    def height(self): return self._widget_base_frame.height()
    @property
    def x(self): return self._widget_base_frame.x()
    @property
    def y(self): return self._widget_base_frame.y()

    def set_position(self, x, y):
        self._widget_base_frame.setGeometry(x, y, self.width, self.height)

    def set_size(self, width, height):
        self._widget_base_frame.setGeometry(self.x, self.y, width, height)

    def show(self): self._widget_base_frame.show()
    def hide(self): self._widget_base_frame.hide()

    def _get_holder(self):
        return self._widget_base_frame

    def get_dpi(self): return self._properties['parent'].get_dpi()

    def set(self, property_name, value):
        self._properties[property_name] = value

        if property_name == 'excess_color':
            self._widget_base_frame.setStyleSheet(f"background-color: {get_as_qt(self._properties['excess_color'])};")

    def get(self, property_name):
        return self._properties[property_name]
