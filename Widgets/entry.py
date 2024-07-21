from PyQt6.QtWidgets import QLineEdit
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes


class Entry(Misc):
    def __init__(self,
                 parent,
                 # Special
                 text       : str       = None,
                 text_size  : str | int = None,
                 font       : str       = None,
                 width      : int | str = None,
                 height     : int | str = None,
                 command    : lambda: ... = None,

                 # Stylesheet
                 text_color      : str = None,
                 background_color: str = None,
                 corner_roundness: str | int = None,
                 hover_color     : str = None,
                 clicked_color   : str = None,

                 border_width    : str | int = None,
                 border_color    : str       = None):

        # Reloader setup
        def text_func(v):
            self._widget.setText(v)

        base = f"""QLineEdit {{ background-color: {V}background_color{V}; border: {V}border_width{V} solid {V}border_color{V}; font-family: {V}font{V}; font-size: {V}text_size{V}; color: {V}text_color{V}; border-radius: {V}corner_roundness{V}; }}
QLineEdit:hover {{ background-color: {V}hover_color{V}; }}
QLineEdit:focus {{ background-color: {V}clicked_color{V}; }}"""

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'border_width': border_width,  'border_color': border_color,  'hover_color': hover_color,   'clicked_color': clicked_color,    'command': command,     'corner_roundness': corner_roundness, 'background_color': background_color, 'text_color': text_color,   'text_size': text_size,     'font': font,         'text': text,              'parent': parent,   'width': width,          'height': height,},
                                  process_types     = {'border_width': 'px-value',    'border_color': 'color',       'hover_color': 'color',       'clicked_color': 'color',          'command': 'super raw', 'corner_roundness': 'px-value',       'background_color': 'color',          'text_color': 'color',      'text_size': 'px-value',    'font': 'raw',        'text': 'raw',             'parent': None,     'width': 'px-value;int', 'height': 'px-value;int'},
                                  default_values    = {'border_width': '0.0105 inch', 'border_color': 'litecrimson', 'hover_color': 'litecrimson', 'clicked_color': 'delightcrimson', 'command': lambda: ..., 'corner_roundness': '0.04 inch',      'background_color': 'crimson',        'text_color': 'white',      'text_size': '0.20 inch',   'font': 'Verdana',    'text': 'Trilent Entry.',  'parent': None,     'width': '1.75 inch',    'height': '0.45 inch'},
                                  property_types    = {'border_width': 'stylesheet',  'border_color': 'stylesheet',  'hover_color': 'stylesheet',  'clicked_color': 'stylesheet',     'command': 'access',    'corner_roundness': 'stylesheet',     'background_color': 'stylesheet',     'text_color': 'stylesheet', 'text_size': 'stylesheet',  'font': 'stylesheet', 'text': 'special',         'parent': 'access', 'width': 'special',      'height': 'special'},
                                  special_functions = {'text': text_func,  'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
                                  base              = base)

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        # noinspection PyProtectedMember
        self._widget = QLineEdit(self._reloader.cp['parent']._get_holder())
        self._widget.setText(self._reloader.cp['text'])

        # Setup properties
        self._widget.setStyleSheet(self._reloader.reload())
        self._widget.editingFinished.connect(lambda: self._reloader.cp['command']())

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)

    def get(self, property_name):
        if property_name == 'text':
            return self._widget.text()
        return self._reloader.cp[property_name]
