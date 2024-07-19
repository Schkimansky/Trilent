from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes


class Image(Misc):
    def __init__(self,
                 parent,
                 # Special
                 image_path  : str,
                 width       : int | str = None,
                 height      : int | str = None,
                 auto_size   : bool      = None,  # Controls if you don't want to enter width and height

                 # Stylesheet
                 background_color: str = None):

        # Reloader setup
        def image_func(v):
            pixmap = QPixmap(v)
            if self._reloader.cp['auto_size']:
                self._widget.adjustSize()

            size = self._reloader.process('width', self._reloader.cp['width']), self._reloader.process('height', self._reloader.cp['height'])

            pixmap = pixmap.scaled(*size)
            self._widget.setPixmap(pixmap)

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'background_color': background_color, 'auto_size': auto_size,   'image_path': image_path, 'parent': parent,   'width': width,          'height': height},
                                  process_types     = {'background_color': 'color',          'auto_size': 'super raw', 'image_path': 'raw',      'parent': None,     'width': 'px-value;int', 'height': 'px-value;int'},
                                  default_values    = {'background_color': 'transparent',    'auto_size': True,        'image_path': None,       'parent': None,     'width': '1 inch',       'height': '1 inch'},
                                  property_types    = {'background_color': 'stylesheet',     'auto_size': 'access',    'image_path': 'special',  'parent': 'access', 'width': 'special',      'height': 'special'},
                                  special_functions = {'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v), 'image_path': image_func},
                                  base              = f"background-color: {V}background_color{V}")

        # Protected widget specific members
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        self._widget = QLabel(self._reloader.cp['parent']._get_holder())
        self._widget.setStyleSheet(self._reloader.reload())

        # Check if Box's parent is also a box
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            self._reloader.cp['parent']._widget_box_add(self)
