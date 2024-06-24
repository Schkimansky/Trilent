from enum import Enum
from PyQt5.QtWidgets import QFrame
from Trilent.Utility import get_in_pixels, Reloader, WidgetTypes


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'
    NONE: str = 'None specified.'


class Widget:
    def __init__(self,
                 parent,
                 width: int | str,
                 height: int | str,
                 excess_color: str = None):

        # Stylesheet manager
        self.__reloader = Reloader(WidgetTypes.WIDGET, parent.get_dpi(), parent=parent, width=width, height=height,
                                   excess_color=excess_color)

        self._position_self = self.__reloader.properties['parent']._position_children
        self._position_children = PositionTypes.NONE

        self.__widget = QFrame(parent._get_holder())
        self.__widget.setGeometry(0, 0, get_in_pixels(width, parent.get_dpi()), get_in_pixels(height, parent.get_dpi()))
        self.__reloader.reload_start()
        self.__widget.setStyleSheet(self.__reloader.stylesheet)

        if self.__reloader.properties['parent']._position_children == PositionTypes.BOX:
            parent._widget_box_add(self)

    def place(self, x: int = 100, y: int = 100):
        assert self.__reloader.properties['parent']._position_self != PositionTypes.BOX, \
            TypeError("You cant place a widget whose parent is a box. Instead, Its position is automatically handled.")

        geometry = self.__widget.geometry()
        self.__widget.setGeometry(x, y, geometry.width(), geometry.height())
        self.__widget.show()

    def force_place(self, x: int = 100, y: int = 100):
        geometry = self.__widget.geometry()
        self.__widget.setGeometry(x, y, geometry.width(), geometry.height())
        self.__widget.show()

    @property
    def width(self): return self.__widget.width()
    @property
    def height(self): return self.__widget.height()
    @property
    def x(self): return self.__widget.x()
    @property
    def y(self): return self.__widget.y()

    def set_position(self, x, y):
        self.__widget.setGeometry(x, y, self.width, self.height)

    def set_size(self, width, height):
        self.__widget.setGeometry(self.x, self.y, width, height)

    def show(self): self.__widget.show()
    def hide(self): self.__widget.hide()

    def _get_holder(self):
        return self.__widget

    def get_dpi(self): return self.__reloader.properties['parent'].get_dpi()

    def set(self, property_name, value):
        self.__reloader.reload(property_name, value)

        self.__widget.setStyleSheet(self.__reloader.stylesheet)

    def get(self, property_name):
        return self.__reloader.properties[property_name]
