import cProfile

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtGui import QPalette, QColor
from Trilent.Utility.unit import get_in_pixels
from functools import lru_cache


def has_parameter(func, param_names):
    return any(param_name in func.__code__.co_varnames for param_name in param_names)


class Window:
    _app: QApplication = QApplication([])
    _window: QMainWindow = QMainWindow()

    def __init__(self,
                 # Utility
                 title: str = 'Trilent Window',
                 width: int | str = '8 inch',
                 height: int | str = '5 inch',
                 x: int | str = '4 inch',
                 y: int | str = '3 inch',
                 # Color
                 background_color='#212121'):

        super().__init__()
        self._update_timer = None
        self._previous_time = None
        self._position_self = PositionTypes.PLACE
        self._position_children = PositionTypes.PLACE
        self._dpi = self.get_dpi()
        self._update_functions = []

        palette = self._window.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(background_color))
        self._window.setPalette(palette)
        self._window.setAutoFillBackground(True)

        self._window.setWindowTitle(title)
        self._window.setGeometry(get_in_pixels(x, self._dpi), get_in_pixels(y, self._dpi), get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

    # Basic Methods
    def run(self, update=None, start=None, update_speed: int = 0):
        if update is not None:
            if has_parameter(update, ['delta', 'delta_time', 'elapsed_time', 'render_time', 'time_took_to_render']):
                self._previous_time = QTime.currentTime()

                def delta_update():
                    current_time = QTime.currentTime()
                    delta_time = self._previous_time.msecsTo(current_time) / 1000.0
                    self._previous_time = current_time
                    update(delta_time)

                self._update_functions.append(delta_update)
            else:
                self._update_functions.append(update)
        if self._update_functions:
            self._update_timer = QTimer(self._window)

            def update_func():
                for func in self._update_functions:
                    func()

            self._update_timer.timeout.connect(update_func)
            self._update_timer.start(update_speed)
        if start is not None: QTimer(self._window).singleShot(0, start)

        self._window.show()
        self._app.exec()

    # Utility Methods
    def close(self): self._app.quit()

    @lru_cache
    def get_dpi(self): return int(self._app.primaryScreen().logicalDotsPerInchX())

    def get_size(self): return self.width, self.height

    @property
    def x(self): return self._window.x()
    @property
    def y(self): return self._window.y()
    @property
    def width(self): return self._window.size().width()
    @property
    def height(self): return self._window.size().height()

    def add_update_function(self, func): self._update_functions.append(func)
    def _get_holder(self): return self._window


if __name__ == "__main__":
    from Trilent.Widgets import *

    window = Window()

    Button(window, text_color='white')

    window.run()
