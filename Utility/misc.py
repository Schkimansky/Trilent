from enum import Enum
from trilent.Animations import Animation
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt, QBuffer, QIODevice
from PyQt6.QtSvg import QSvgGenerator
from .color import get_as_raw_qt
from typing import Any
from numpy import array


key_map = {
    Qt.Key.Key_Up: "up",
    Qt.Key.Key_Down: "down",
    Qt.Key.Key_Left: "left",
    Qt.Key.Key_Right: "right",
    Qt.Key.Key_Space: "space",
    Qt.Key.Key_Return: "enter",
    Qt.Key.Key_Backspace: "backspace",
    Qt.Key.Key_Tab: "tab",
    Qt.Key.Key_Escape: "escape",
    Qt.Key.Key_Delete: "delete",
    Qt.Key.Key_Home: "home",
    Qt.Key.Key_End: "end",
    Qt.Key.Key_PageUp: "page up",
    Qt.Key.Key_PageDown: "page down",
    Qt.Key.Key_CapsLock: "caps lock",
    Qt.Key.Key_Shift: "shift",
    Qt.Key.Key_Control: "control",
    Qt.Key.Key_Alt: "alt",
    Qt.Key.Key_Meta: "meta"
}


def get_event_as_text(e):
    text = e.text()
    if text:
        return text
    else:
        return key_map.get(e.key(), 'unknown')


events_dictionary: dict[str, str] = {'wheel': 'wheelEvent',
                                     'drag': 'mouseMoveEvent',
                                     'hover': 'enterEvent',
                                     'unhover': 'leaveEvent',
                                     'clicked': 'mousePressEvent',
                                     'unclicked': 'mouseReleaseEvent',
                                     'key press': 'keyPressEvent'}


events_mappers: dict[str, Any] = {'wheel': lambda e, f: f(),
                                  'drag': lambda e, f: f(),
                                  'hover': lambda e, f: f(),
                                  'unhover': lambda e, f: f(),
                                  'clicked': lambda e, f: f(),
                                  'unclicked': lambda e, f: f(),
                                  'key press': lambda e, f: f(get_event_as_text(e))}


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'
    NONE: str = 'None specified.'


class Misc:
    def __init__(self):
        self._widget = QPushButton()

    def place(self, x: int = 100, y: int = 100):
        assert self._reloader.cp['parent']._position_children != PositionTypes.BOX, \
            TypeError("You cant place a widget whose parent is a box. Instead, Its position is automatically handled.")

        geometry = self._widget.geometry()
        self._widget.setGeometry(x, y, geometry.width(), geometry.height())
        self._widget.show()

    def force_place(self, x: int = 100, y: int = 100):
        geometry = self._widget.geometry()
        self._widget.setGeometry(x, y, geometry.width(), geometry.height())
        self._widget.show()

    def set_tooltip(self, tooltip): self._widget.setToolTip(tooltip)
    def get_tooltip(self): self._widget.toolTip()

    def set_position(self, x, y): self._widget.setGeometry(x, y, self.width, self.height)
    def set_size(self, width, height): self._widget.setGeometry(self.x, self.y, width, height)

    def get_position(self):
        geometry = self._widget.geometry()
        return geometry.x(), geometry.y()

    def get_size(self):
        geometry = self._widget.geometry()
        return geometry.width(), geometry.height()

    def change(self, **kwargs):
        for k, v in kwargs.items():
            self._reloader.set(k, v)

        self._widget.setStyleSheet(self._reloader.reload())

    def set(self, name, value):
        self._reloader.set(name, value)

        ss = self._reloader.reload()

        if self._reloader.initial_parameters['property_types'][name] == 'stylesheet':
            self._widget.setStyleSheet(ss)

    def get(self, property_name):
        return self._reloader.cp[property_name]

    @property
    def width(self): return self._widget.width()
    @property
    def height(self): return self._widget.height()
    @property
    def x(self): return self._widget.x()
    @property
    def y(self): return self._widget.y()

    def show(self): self._widget.show()
    def hide(self): self._widget.hide()

    def is_hidden(self): return self._widget.isHidden()
    def is_shown(self): return not self._widget.isHidden()

    def get_top_parent(self): return self.get('parent').get_top_parent()

    def connect(self, name, func):
        caller = lambda e: events_mappers[name](e, func)
        setattr(self._widget, events_dictionary[name], caller)

    def animate(self, time=0.3, curve='ease in out', animation_finished=lambda: ..., mode='', **kwargs):
        for i, (k, v) in enumerate(kwargs.items()):
            Animation(self, k, v, time=time, curve=curve, mode=mode, animation_finished=animation_finished if i == 0 else lambda: ...).start()

    def effect(self, name, **kwargs):
        if name == "shadow":
            blur, x,  y, color = kwargs['blur'], kwargs['x'], kwargs['y'], kwargs['color']
            effect = QGraphicsDropShadowEffect()
            effect.setXOffset(x)
            effect.setYOffset(y)
            effect.setBlurRadius(blur)
            effect.setColor(QColor(*get_as_raw_qt(color)))

            self._widget.setGraphicsEffect(effect)

    def remove_effects(self):
        self._widget.setGraphicsEffect(None)

    def enable(self): self._widget.setDisabled(False)
    def disable(self): self._widget.setDisabled(True)

    def add_update_function(self, f):
        self.get_top_parent().add_update_function(f)

    def get_pixel_data(self):
        pixmap = self._widget.grab()

        image = pixmap.toImage()

        width = image.width()
        height = image.height()

        ptr = image.bits()
        ptr.setsize(image.sizeInBytes())
        arr = array(ptr).reshape((height, width, 4))

        return arr

    def get_as_svg(self):
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.ReadWrite)

        svg_generator = QSvgGenerator()
        svg_generator.setOutputDevice(buffer)
        svg_generator.setSize(self._widget.size())
        svg_generator.setViewBox(self._widget.rect())
        svg_generator.setTitle("Widget as SVG")
        svg_generator.setDescription("Trilent SVG")

        painter = QPainter(svg_generator)
        self._widget.render(painter)
        painter.end()

        buffer.seek(0)
        return buffer.readData(buffer.size()).decode()

    def delete(self):
        self._widget.setParent(None)
