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
        self._position_self = PositionTypes.PLACE
        self._position_children = PositionTypes.PLACE
        self._dpi = self.get_dpi()
        self._update_functions = []

        if background_color != 'white':
            self._window.setStyleSheet(f"background-color: {get_as_qt(background_color)};")

        self._window.setWindowTitle(title)
        self._window.setGeometry(get_in_pixels(x, self._dpi), get_in_pixels(y, self._dpi),
                                 get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

    # Basic Methods
    def run(self, update=None, start=None, update_speed: int = 0):
        if update is not None:
            self._update_functions.append(update)

        if self._update_functions:
            self._update_timer = QTimer(self._window)

            def update_all(functions): [func() for func in functions]

            self._update_timer.timeout.connect(lambda: update_all(self._update_functions))
            self._update_timer.start(update_speed)

        if start is not None:
            QTimer(self._window).singleShot(0, start)

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

    def add_update_function(self, func):
        self._update_functions.append(func)

    # Protected Library use case Methods
    def _get_holder(self): return self._window


if __name__ == "__main__":
    from Trilent.Widgets import Widget, Box, Text

    window = Window()

    box = Box(window, alignment='start', side_alignment='center', gap=5, vertical_gap=5)
    box.place(0, 0)

    text = Text(box, text='Cool', text_size='20 px')
    text.place(0, 0)

    window.run()
