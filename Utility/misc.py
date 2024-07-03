from enum import Enum


class PositionTypes(Enum):
    BOX: str = 'box'
    PLACE: str = 'place'
    NONE: str = 'None specified.'


class Misc:
    def place(self, x: int = 100, y: int = 100):
        assert self._reloader.cp['parent']._position_self != PositionTypes.BOX, \
            TypeError("You cant place a widget whose parent is a box. Instead, Its position is automatically handled.")

        geometry = self._widget.geometry()
        self._widget.setGeometry(x, y, geometry.width(), geometry.height())
        self._widget.show()

    def force_place(self, x: int = 100, y: int = 100):
        geometry = self._widget.geometry()
        self._widget.setGeometry(x, y, geometry.width(), geometry.height())
        self._widget.show()

    def set_position(self, x, y): self._widget.setGeometry(x, y, self.width, self.height)
    def set_size(self, width, height): self._widget.setGeometry(self.x, self.y, width, height)

    def show(self): self._widget.show()
    def hide(self): self._widget.hide()

    def change(self, **kwargs):
        for k, v in kwargs.items():
            self._reloader.set(k, v)

        self._widget.setStyleSheet(self._reloader.reload())

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
