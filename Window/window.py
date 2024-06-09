import cProfile
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QTimer
from Trilent.Utility import get_in_pixels, get_as_qt
from cProfile import run


class Window:
    _app = QApplication(sys.argv)
    _window = QMainWindow()

    def __init__(self,
                 # Utility
                 title: str = 'Trilent Window',
                 width: int | str = '8 inch',
                 height: int | str = '5 inch',
                 x: int | str = '5 inch',
                 y: int | str = '3 inch',
                 # Color
                 background_color='white'):

        super().__init__()
        self._update_timer = None

        if background_color != 'white':
            self._window.setStyleSheet(f"background-color: {get_as_qt(background_color)};")
        self._window.setWindowTitle(title)
        self._window.setGeometry(get_in_pixels(x), get_in_pixels(y), get_in_pixels(width), get_in_pixels(height))

    def run(self, update=None, start=None, update_speed: int = 0):
        if update:
            self._update_timer = QTimer(self._window)
            self._update_timer.timeout.connect(update)
            self._update_timer.start(update_speed)
        if start:
            self._window.showEvent = lambda event: start()

        self._window.show()
        sys.exit(self._app.exec_())

    def close(self):
        self._app.quit()


def main():
    window = Window()

    window.run(start=lambda: window.close())


if __name__ == "__main__":
    main()
