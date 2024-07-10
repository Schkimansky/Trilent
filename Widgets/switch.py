from Trilent.Widgets import Slider
from typing import Literal
from PyQt6.QtCore import Qt
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

        super().__init__(parent, width, height, command, 1, modes, 1, unfilled_color, button_color, filled_color, orientation, corner_roundness=corner_roundness, handle_corner_roundness=handle_corner_roundness)

        self._state = starting_state

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

    def mouseMoveEvent(self, event):
        # Ignore mouse move event to prevent the handle from being moved
        event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Increment the state and wrap around if it exceeds the modes
            self._state = self._widget.value() + 1
            if self._state > self._widget.maximum():
                self._state = self._widget.minimum()
            self._widget.setValue(self._state)

        super(QSlider, self._widget).mouseReleaseEvent(event)
