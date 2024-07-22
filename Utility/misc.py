from enum import Enum
from trilent.Animations import Animation

events_dictionary: dict[str, str] = {'wheel': 'wheelEvent',
                                     'drag': 'mouseMoveEvent',
                                     'hover': 'enterEvent',
                                     'unhover': 'leaveEvent',
                                     'clicked': 'mousePressEvent',
                                     'unclicked': 'mouseReleaseEvent'}


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'
    NONE: str = 'None specified.'


class Misc:
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

    def connect(self, name, func): setattr(self._widget, events_dictionary[name], lambda e: func())

    def animate(self, time=0.3, curve='ease in out', animation_finished=lambda: ..., mode='', **kwargs):
        for i, (k, v) in enumerate(kwargs.items()):
            Animation(self, k, v, time=time, curve=curve, mode=mode, animation_finished=animation_finished if i == 0 else lambda: ...).start()

    def enable(self): self._widget.setDisabled(False)
    def disable(self): self._widget.setDisabled(True)
