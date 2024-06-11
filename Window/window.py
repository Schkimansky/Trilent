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

    @lru_cache
    def get_dpi(self): return self._app.desktop().logicalDpiX()

    def _widget_box_add(self, trilent_widget):
        raise RuntimeError('Place mode was overriden as box mode')

    def _get_holder(self): return self._window


if __name__ == "__main__":
    from Trilent.Widgets import Widget, Box
    window = Window()

    print('Setting box')
    box = Box(window, 200, 200, background_color='red')
    print('Placing box')
    box.place(100, 100)

    print('Setting sub box / widget')
    box2 = Box(box, 100, 100, background_color='green')
    widget = Widget(box2, 70, 70, excess_color='yellow')

    window.run()
