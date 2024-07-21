from PyQt6.QtWidgets import QCheckBox
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes


class CheckBox(Misc):
    def __init__(self,
                 parent,
                 # Special
                 width: int | str = None,
                 height: int | str = None,
                 command: lambda: ... = None,
                 text: str = None,
                 text_size: int | str = None,
                 font: str = None,  # Add font parameter

                 # Stylesheet
                 checked_color: str = None,
                 unchecked_color: str = None,
                 text_color: str = None,
                 corner_roundness: str | int = None):
        # Reloader setup
        base = \
f"""QCheckBox::indicator:checked {{
    background-color: {V}checked_color{V};
}}
QCheckBox::indicator:unchecked {{
    background-color: {V}unchecked_color{V};
}}
QCheckBox {{
    color: {V}text_color{V};
    font-size: {V}text_size{V};
    font-family: {V}font{V};
    background-color: rgba(0,0,0,0);
}}
QCheckBox::indicator {{
    border-radius: {V}corner_roundness{V};
}}
"""

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties={'checked_color': checked_color, 'unchecked_color': unchecked_color,
                                                    'text_color': text_color, 'command': command, 'parent': parent,
                                                    'width': width, 'height': height, 'text': text, 'text_size': text_size, 'font': font, 'corner_roundness': corner_roundness},
                                  process_types={'checked_color': 'color', 'unchecked_color': 'color',
                                                 'text_color': 'color', 'command': 'super raw', 'parent': None,
                                                 'width': 'px-value;int', 'height': 'px-value;int', 'text': None, 'text_size': 'px-value', 'font': 'raw', 'corner_roundness': 'px-value'},
                                  default_values={'checked_color': 'cornflowerblue', 'unchecked_color': 'royalblue',
                                                  'text_color': 'white', 'command': lambda: ..., 'parent': None,
                                                  'width': '1.75 inch', 'height': '0.45 inch', 'text': 'Trilent CheckBox.', 'text_size': '13 px', 'font': 'Arial', 'corner_roundness': '2 px'},
                                  property_types={'checked_color': 'stylesheet', 'unchecked_color': 'stylesheet',
                                                  'text_color': 'stylesheet', 'command': 'access', 'parent': 'access',
                                                  'width': 'special', 'height': 'special', 'text': 'access', 'text_size': 'stylesheet', 'font': 'stylesheet', 'corner_roundness': 'stylesheet'},
                                  special_functions={
                                      'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height),
                                      'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
                                  base=base)

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        self._widget = QCheckBox(self._reloader.cp['text'], self._reloader.cp['parent']._get_holder())  # Use text parameter

        # Setup properties
        self._widget.setStyleSheet(self._reloader.reload())
        self._widget.stateChanged.connect(lambda: self._reloader.cp['command']())

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)

    def is_on(self): return self._widget.isChecked()
    def is_mid(self): return self._widget.isTristate()
    def is_off(self): return not self._widget.isChecked()
