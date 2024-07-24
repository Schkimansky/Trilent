from typing import Literal
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QIcon
from trilent.Utility.unit import get_in_pixels
from trilent.Utility.color import get_as_qt
from trilent.Utility.misc import Misc
from functools import lru_cache
from trilent.Widgets.widget import PositionTypes
import os

current_directory = os.path.dirname(os.path.abspath(__file__))


def has_parameter(func, param_names):
    return any(param_name in func.__code__.co_varnames for param_name in param_names)


class Window(Misc):
    _app: QApplication = QApplication([])
    _widget: QMainWindow = QMainWindow()

    def __init__(self,
                 # Utility
                 title: str = 'Trilent Window',
                 width: int | str = '8 inch',
                 height: int | str = '5 inch',
                 x: int | str = '4 inch',
                 y: int | str = '3 inch',
                 # Color
                 background_color='#212121',

                 icon=None,
                 default_icon='empty'):

        self._update_timer = None
        self._previous_time = None
        self._position_self = PositionTypes.PLACE
        self._position_children = PositionTypes.PLACE
        self._dpi = self.get_dpi()
        self._update_functions = []
        self.delta = 1

        default_icon_dict = {'empty': '''<svg width="16" height="16" xmlns="http://www.w3.org/2000/svg"><rect width="16" height="16" fill="none" /><circle cx="8" cy="8" r="1" fill="black" fill-opacity="0.05" /></svg>'''}

        self._widget.setStyleSheet(f'background-color: {get_as_qt(background_color)};')
        self._widget.setWindowTitle(title)
        self._widget.setGeometry(get_in_pixels(x, self._dpi), get_in_pixels(y, self._dpi), get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))
        if icon:
            self.icon(icon)
        else:
            self.icon_data(default_icon_dict[default_icon])

        self._setup_delta_setter()

    # Basic Methods
    def run(self, update=None, start=None, update_speed: int = 0):
        if update is not None:
            if has_parameter(update, ['delta', 'delta_time', 'elapsed_time', 'render_time', 'time_took_to_render']):
                self._update_functions.append(lambda: update(self.delta))
            else:
                self._update_functions.append(update)
        if self._update_functions:
            self._update_timer = QTimer(self._widget)

            def update_func():
                for func in self._update_functions:
                    func()

            self._update_timer.timeout.connect(update_func)
            self._update_timer.start(update_speed)
        if start is not None:
            QTimer(self._widget).singleShot(0, start)

        self._widget.show()
        self._app.exec()

    def attribute(self, name: Literal['opacity', 'transparent', 'show at taskbar'], value, warn=True):
        match name:
            case 'transparent':
                if value:
                    self._widget.setWindowFlags(self._widget.windowFlags() | Qt.WindowType.FramelessWindowHint)
                    self._widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
                else:
                    self._widget.setWindowFlags(self._widget.windowFlags() | Qt.WindowType.Window)
                    self._widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
                    self._widget.show()
            case 'opacity':
                self._log('Opacity may glitch slightly in Windows.', warn)
                self._widget.setWindowOpacity(value / 100)
            case 'show at taskbar':
                if value:
                    self._widget.setWindowFlags(self._widget.windowFlags() | Qt.WindowType.Window)
                else:
                    self._widget.setWindowFlags(self._widget.windowFlags() | Qt.WindowType.Tool)
                self._log('"Show at taskbar" may remove the starting animation of the window', warn)

    @staticmethod
    def _log(string, warn):
        if warn:
            print(string)
            print('To disable this warning, Set warn=False')

    # Utility Methods
    def close(self): self._app.quit()
    @lru_cache
    def get_dpi(self): return int(self._app.primaryScreen().logicalDotsPerInchX())

    def add_update_function(self, func, parse_delta=False):
        if not parse_delta:
            self._update_functions.append(func)
        else:
            self._update_functions.append(lambda: func(self.delta))

    def remove_update_function(self, func):
        self._update_functions = [f for f in self._update_functions if not (callable(f) and f.__closure__ and f.__closure__[0].cell_contents == func)]

    def after(self, ms, func): QTimer(self._widget).singleShot(ms, func)

    def fullscreen(self): self._widget.showFullScreen()
    def normal(self): self._widget.show()
    def minimize(self): self._widget.showMinimized()
    def maximize(self): self._widget.showMaximized()

    def icon(self, path):
        icon = QIcon(path)
        self._widget.setWindowIcon(icon)

    def icon_data(self, svg_data):
        with open(os.path.join(current_directory, 'cache.svg'), 'w') as f:
            f.write(svg_data)

        self.icon(os.path.join(current_directory, 'cache.svg'))

    def title(self, title): self._widget.setWindowTitle(title)
    def background_color(self, background_color): self._widget.setStyleSheet(f'background-color: {background_color};')

    def _get_holder(self): return self._widget

    def get_top_parent(self): return self

    def _setup_delta_setter(self):
        self._previous_time = QTime.currentTime()

        def delta_update():
            current_time = QTime.currentTime()
            delta_time = self._previous_time.msecsTo(current_time) / 1000.0
            self._previous_time = current_time
            self.delta = delta_time

        self._update_functions.append(delta_update)
