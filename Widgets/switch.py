from trilent.Widgets import Slider
from typing import Literal
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QSlider


class Switch(Slider):
    def __init__(self,
                 parent,
                 # Special
                 width      : int | str = '0.45 inch',
                 height     : int | str = None,
                 command    : lambda: ... = None,

                 # Access
                 modes      : str | int = 2,

                 # Stylesheet
                 unfilled_color  : str = None,
                 button_color    : str = None,
                 filled_color    : str = None,

                 orientation            : Literal['horizontal', 'vertical'] = 'horizontal',
                 corner_roundness       : str | int = None,
                 handle_corner_roundness: str | int = None,

                 # Kick starters
                 starting_state         : int = 1):

        if handle_corner_roundness is None:
            handle_corner_roundness = 15 // 2

        super().__init__(parent, width, height, command, 1, modes, 1, unfilled_color, button_color, filled_color, orientation, corner_roundness=corner_roundness, handle_corner_roundness=handle_corner_roundness)

        self._state = starting_state
        self._modes = modes

        self._moveHandled = False

        # Make it behave like a toggler instead of a picker
        self._widget.mousePressEvent = self.mousePressEvent
        self._widget.mouseReleaseEvent = self.mouseReleaseEvent
        self._widget.mouseMoveEvent = self.mouseMoveEvent

    def mousePressEvent(self, event):
        # Ignore mouse press event to prevent the handle from being moved
        if event.button() == Qt.MouseButton.LeftButton:
            event.ignore()
            return
        super(QSlider, self._widget).mousePressEvent(event)

    @staticmethod
    def find_closest_number(array, target):
        closest_num = array[0]
        min_diff = abs(array[0] - target)

        for num in array:
            diff = abs(num - target)
            if diff < min_diff:
                min_diff = diff
                closest_num = num

        return closest_num

    def mouseMoveEvent(self, event: QEvent):
        x = event.pos().x()
        width = self._widget.width()
        new_value = (x / width) * (self._widget.maximum() - self._widget.minimum()) + self._widget.minimum()

        width_mappings = [i for i in range(((self._widget.maximum() - self._widget.minimum()) + self._widget.minimum()) + 1)]

        closest_value = self.find_closest_number(width_mappings, new_value)

        self._widget.setValue(int(closest_value))

        self._moveHandled = True

        event.accept()

    def mouseReleaseEvent(self, event):
        if not self._moveHandled:
            if event.button() == Qt.MouseButton.LeftButton:
                # Increment the state and wrap around if it exceeds the modes
                self._state = self._widget.value() + 1
                if self._state > self._widget.maximum():
                    self._state = self._widget.minimum()
                self._widget.setValue(self._state)

            super(QSlider, self._widget).mouseReleaseEvent(event)
        else:
            self._moveHandled = False
