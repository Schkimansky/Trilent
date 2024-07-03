from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer, QTime
from Trilent.Utility import get_in_pixels, get_as_qt
from functools import lru_cache
from Trilent.Widgets import PositionTypes
from inspect import signature


def has_parameter(func, param_names):
    return any(param_name in signature(func).parameters for param_name in param_names)


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
                 background_color='#272727'):

        super().__init__()
        self._previous_time = None
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

            self._update_timer.timeout.connect(lambda: tuple(func() for func in self._update_functions))
            self._update_timer.start(update_speed)

        if start is not None:
            QTimer(self._window).singleShot(0, start)

        self._window.show()
        self._app.exec()

    def close(self):
        self._app.quit()

    # Utility Methods
    @lru_cache
    def get_dpi(self): return int(self._app.primaryScreen().logicalDotsPerInchX())

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
    from Trilent.Widgets import Box, Widget, Text, Button


    class MyApp:
        def __init__(self):
            self.window = Window()
            self.box = Box(self.window, alignment='start', side_alignment='start', gap=1, vertical_gap=1, corner_roundness=1, background_color='transparent')
            self.box.place(0, 0)

            self.button = Button(self.box, text='Download')

            self.box.set_size(self.window.width, self.window.height)

            self.time = 0
            self.fpses = []

        def update(self, delta):
            delta += 0.001  # Prevent zero division error
            self.fpses.append(1 / delta)
            self.time += delta

            if self.time >= 10:
                self.time = 0
                print(f'FPS: {sum(self.fpses) / len(self.fpses)}')
                self.fpses = []

            self.box.set_size(self.window.width, self.window.height)

        def run(self):
            self.window.run(self.update)

    app = MyApp()
    app.run()