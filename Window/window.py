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
                 background_color='#212121'):

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
    import Trilent.Widgets as tri
    import keyboard as kb
    from uuid import uuid4

    class MyApp:
        def __init__(self):
            self.window = Window('Animation', '10 inch', '6 inch', 340, 200)
            self.fpses = []
            self.time = 0
            self.squares = []
            self.acc = [0, 0]

            self.build()
            self.window.run(self.update)

        def build(self):
            self.box = tri.Box(self.window, width=self.window.width, height=self.window.height, alignment='center', side_alignment='center')

            tri.CheckBox(self.box, text='Deterministic')

            self.gap_slider = tri.Slider(self.window, command=self.update_gap)
            self.gap_slider.place(18, self.window.height - 50)

            self.fps_text = tri.Text(self.window, text='FPS: ....', text_size=13)
            self.fps_text.place(200, self.window.height - 36)

            WIDTH = 10
            HEIGHT = 10
            ROUNDING = WIDTH // 13
            AMOUNT = 10
            self.SPEED = 1

            COLOR = 'cornflowerblue'

            for _ in range(AMOUNT):
                self.squares.append(tri.Widget(self.box, WIDTH, HEIGHT, COLOR, ROUNDING))

        def update_gap(self, value):
            self.box.change(gap=value, vertical_gap=value)

        def update(self, delta):
            delta += 0.00001

            self.fpses.append(1 / delta)
            self.time += delta

            if self.time >= 1:
                fps = sum(self.fpses) / len(self.fpses)
                self.fps_text.change(text=f"FPS: {fps:.0f}")
                self.fpses = []
                self.time = 0

            self.box.set_position(self.box.x + self.acc[0], self.box.y + self.acc[1])

            self.box.set_size(self.window.width, self.window.height)
            self.gap_slider.set_position(18, self.window.height - 50)
            self.fps_text.set_position(self.window.width - (9 * len(self.fps_text.get('text'))), self.window.height - 36)

    MyApp()
