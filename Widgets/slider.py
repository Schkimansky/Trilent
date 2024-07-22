from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes
from typing import Literal


class Slider(Misc):
    def __init__(self,
                 parent,
                 # Special
                 width: int | str = None,
                 height: int | str = None,
                 command: lambda: ... = None,
                 minimum: int = None,
                 maximum: int = None,

                 # Access
                 quality: str | int = None,

                 # Stylesheet
                 unfilled_color: str = None,
                 button_color: str = None,
                 filled_color: str = None,

                 orientation: Literal['horizontal', 'vertical'] = 'horizontal',
                 corner_roundness: str | int = None,
                 handle_corner_roundness: str | int = None,

                 # Kick starters
                 starting_value: int = 0):

        # Reloader setup
        base = f"""QSlider {{ background-color : rgba(0, 0, 0, 0); }}

QSlider::handle {{
    background-color: {V}button_color{V};
    border-radius: {V}handle_corner_roundness{V};
}}
QSlider::sub-page {{
    background-color: {V}filled_color{V};
    border-radius: {V}corner_roundness{V};
}}
QSlider::add-page {{
    background-color: {V}unfilled_color{V};
    border-radius: {V}corner_roundness{V};
}}
"""

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties={'corner_roundness': corner_roundness, 'handle_corner_roundness': handle_corner_roundness, 'minimum': minimum, 'maximum': maximum, 'quality': quality, 'orientation': orientation, 'filled_color': filled_color, 'button_color': button_color, 'command': command, 'unfilled_color': unfilled_color, 'parent': parent, 'width': width, 'height': height,},
                                  process_types={'corner_roundness': 'px-value', 'handle_corner_roundness': 'px-value', 'minimum': 'super raw', 'maximum': 'super raw', 'quality': 'px-value;int', 'orientation': 'raw', 'filled_color': 'color', 'button_color': 'color', 'command': 'super raw', 'unfilled_color': 'color', 'parent': None, 'width': 'px-value;int', 'height': 'px-value;int'},
                                  default_values={'corner_roundness': '0.022 inch', 'handle_corner_roundness': '0.04 inch', 'minimum': 0, 'maximum': 100, 'quality': 1, 'orientation': 'horizontal', 'filled_color': 'cornflowerblue', 'button_color': 'white', 'command': lambda v: ..., 'unfilled_color': 'royalblue', 'parent': None, 'width': '1.75 inch', 'height': '0.45 inch'},
                                  property_types={'corner_roundness': 'stylesheet', 'handle_corner_roundness': 'stylesheet', 'minimum': 'special', 'maximum': 'special', 'quality': 'access', 'orientation': 'special', 'filled_color': 'stylesheet', 'button_color': 'stylesheet', 'command': 'access', 'unfilled_color': 'stylesheet', 'parent': 'access', 'width': 'special', 'height': 'special'},
                                  special_functions={'minimum': lambda v: self._widget.setMinimum(v), 'maximum': lambda v: self._widget.setMaximum(v), 'orientation': lambda v: self._widget.setOrientation(self._orientations[v]), 'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
                                  base=base)

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        # noinspection PyProtectedMember
        self._orientations = {'horizontal': Qt.Orientation.Horizontal, 'vertical': Qt.Orientation.Vertical}
        self._widget = QSlider(self._orientations[orientation], self._reloader.cp['parent']._get_holder())

        def slider_command(v: int):
            v = (v // self._reloader.cp['quality']) * self._reloader.cp['quality']
            self._widget.setValue(v)
            self._reloader.cp['command'](v)

        # Setup properties
        self._widget.setValue(starting_value)
        self._widget.setStyleSheet(self._reloader.reload())
        self._widget.valueChanged.connect(slider_command)

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)
