from PyQt6.QtWidgets import QLabel
from trilent.Utility import Reloader, qt_orientation, V, Misc
from trilent.Widgets import PositionTypes


class Text(Misc):
    def __init__(self,
                 parent,
                 # Special
                 text       : str       = None,
                 orientation: str       = None,
                 text_size  : str | int = None,
                 font       : str       = None,
                 width      : int | str = None,
                 height     : int | str = None,
                 auto_size  : bool      = None,  # Controls if you don't want to enter width and height
                 wrap       : bool      = None,

                 # Stylesheet
                 text_color      : str = None,
                 background_color: str = None):

        # Reloader setup
        def text_func(v):
            if self._reloader.cp['auto_size'] is True:
                self._widget.adjustSize()

            self._widget.setText(v)

        def orient_func(v): self._widget.setAlignment(v)

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'wrap': wrap,                                  'background_color': background_color, 'text_color': text_color,   'auto_size': auto_size,   'text_size': text_size,     'font': font,         'orientation': orientation,   'text': text,            'parent': parent,   'width': width,          'height': height,},
                                  process_types     = {'wrap': 'super raw',                           'background_color': 'color',          'text_color': 'color',      'auto_size': 'super raw', 'text_size': 'px-value',    'font': 'raw',        'orientation': 'orientation', 'text': 'raw',           'parent': None,     'width': 'px-value;int', 'height': 'px-value;int'},
                                  default_values    = {'wrap': True,                                  'background_color': 'transparent',    'text_color': 'white',      'auto_size': False,       'text_size': '0.3 inch',    'font': 'Arial',      'orientation': 'top left',    'text': 'Trilent Text.', 'parent': None,     'width': '5 inch',       'height': '0.5 inch'},
                                  property_types    = {'wrap': 'special',                             'background_color': 'stylesheet',     'text_color': 'stylesheet', 'auto_size': 'access',    'text_size': 'stylesheet',  'font': 'stylesheet', 'orientation': 'special',     'text': 'special',       'parent': 'access', 'width': 'special',      'height': 'special'},
                                  special_functions = {'wrap': lambda v: self._widget.setWordWrap(v), 'orientation':       orient_func,     'text': text_func,          'width' : lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
                                  base              = f"background-color: {V}background_color{V}; font-family: {V}font{V}; font-size: {V}text_size{V}; color: {V}text_color{V}")

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        # noinspection PyProtectedMember
        self._widget = QLabel(self._reloader.cp['text'], self._reloader.cp['parent']._get_holder())
        self._widget.setAlignment(qt_orientation(self._reloader.cp['orientation']))

        # Setup properties
        self._widget.setStyleSheet(self._reloader.reload())

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)

