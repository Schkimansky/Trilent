from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QTimer
from Trilent.Utility import get_in_pixels, get_as_qt
from functools import lru_cache
from Trilent.Widgets import PositionTypes


class Window:
    _app: QApplication = QApplication(argv)
    _window: QMainWindow = QMainWindow()

    def __init__(self,
                 # Utility
                 title: str = 'Trilent Window',
                 width: int | str = '8 inch',
                 height: int | str = '5 inch',
                 x: int | str = '4 inch',
                 y: int | str = '3 inch',
                 # Color
                 background_color='#272727'):

        super().__init__()
        self._update_timer = None
        self._positionType = PositionTypes.PLACE
        self._dpi = self.get_dpi()

        if background_color != 'white':
            self._window.setStyleSheet(f"background-color: {get_as_qt(background_color)};")

        self._window.setWindowTitle(title)
        self._window.setGeometry(get_in_pixels(x, self._dpi), get_in_pixels(y, self._dpi),
                                 get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

    # Basic Methods
    def run(self, update=None, start=None, update_speed: int = 0):
        if update is not None:
            self._update_timer = QTimer(self._window)
            self._update_timer.timeout.connect(update)
            self._update_timer.start(update_speed)
        if start is not None:
            timer = QTimer(self._window)
            timer.singleShot(0, start)

        self._window.show()
        self._app.exec_()

    def close(self):
        self._app.quit()

    # Utility Methods
    @lru_cache
    def get_dpi(self): return self._app.desktop().logicalDpiX()

    def get_size(self):
        size = self._window.size()
        return size.width(), size.height()

    # Property Utility Methods
    @property
    def width(self): return self._window.size().width()
    @property
    def height(self): return self._window.size().height()

    # Protected Library use case Methods
    def _widget_box_add(self, trilent_widget): raise RuntimeError('Place mode was overriden as box mode')
    def _get_holder(self): return self._window


if __name__ == "__main__":
    from Trilent.Widgets import Widget, Box
    from Trilent.FlexComputer.main import HorizontalBox
    from random import randint

    #
    # Values
    #

    CHILDREN = 10
    WIDTH = 50
    HEIGHT = WIDTH
    GAP = 1
    VGAP = GAP
    randomness = 0
    WIDGET_COLOR = 'red'
    DOWN_SPEED = 1
    INITIAL_Y_POSITION = 0
    PERCENTAGE = 1.1
    ALIGNMENT = 'start'
    SIDE_ALIGNMENT = 'center'

    window = Window()

    children: list[Widget] = []
    [children.append(Widget(window, WIDTH, HEIGHT + randint(-randomness, randomness), excess_color=WIDGET_COLOR)) for i in range(1, CHILDREN + 1)]

    widths = tuple(child.width for child in children)
    heights = tuple(child.height for child in children)

    def update():
        main_axis = HorizontalBox(widths, heights, window.width, window.height, wrap=True, alignment=ALIGNMENT, side_alignment=SIDE_ALIGNMENT, gap=GAP, vertical_gap=VGAP)

        for i, child in enumerate(children):
            child.set_position(*main_axis[i])


    window.run(update, update)
