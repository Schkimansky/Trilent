from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt
from Trilent.Utility import Reloader, V, Misc
from Trilent.Widgets import PositionTypes
from typing import Literal


class Slider(Misc):
    def __init__(self,
                 parent,
                 # Special
                 width      : int | str = None,
                 height     : int | str = None,
                 command    : lambda: ... = None,

                 # Stylesheet
                 unfilled_color  : str = None,
                 button_color    : str = None,
                 filled_color    : str = None,

                 orientation     : Literal['horizontal', 'vertical'] = 'horizontal'):

        # Reloader setup
        base = \
f"""QSlider::handle {{
    background: {V}button_color{V};
    border-radius: 3px;
}}
QSlider::sub-page {{
    background: {V}filled_color{V};
    border-radius: 3px;
}}
QSlider::add-page {{
    background: {V}unfilled_color{V};
    border-radius: 3px;
}}
"""

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'orientation': orientation,  'filled_color': filled_color,      'button_color': button_color, 'command': command,     'unfilled_color': unfilled_color,   'parent': parent,   'width': width,          'height': height,},
                                  process_types     = {'orientation': 'raw',        'filled_color': 'color',           'button_color': 'color',      'command': 'super raw', 'unfilled_color': 'color',          'parent': None,     'width': 'px-value;int', 'height': 'px-value;int'},
                                  default_values    = {'orientation': 'horizontal', 'filled_color': 'cornflowerblue',  'button_color': 'white',      'command': lambda: ..., 'unfilled_color': 'royalblue',      'parent': None,     'width': '1.75 inch',    'height': '0.45 inch'},
                                  property_types    = {'orientation': 'special',    'filled_color': 'stylesheet',      'button_color': 'stylesheet', 'command': 'access',    'unfilled_color': 'stylesheet',     'parent': 'access', 'width': 'special',      'height': 'special'},
                                  special_functions = {'orientation': lambda v: self._widget.setOrientation(self._orientations[v]), 'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
                                  base              = base)

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        # noinspection PyProtectedMember
        self._orientations = {'horizontal': Qt.Orientation.Horizontal, 'vertical': Qt.Orientation.Vertical}
        self._widget = QSlider(self._orientations[orientation], self._reloader.cp['parent']._get_holder())

        # Setup properties
        self._widget.setStyleSheet(self._reloader.reload())
        self._widget.valueChanged.connect(self._reloader.cp['command'])

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)
