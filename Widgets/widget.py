from PyQt6.QtWidgets import QFrame
from trilent.Utility import Reloader, V, Misc, PositionTypes


class Widget(Misc):
    def __init__(self,
                 parent,
                 width: int | str,
                 height: int | str,
                 widget_color: str = None,
                 corner_roundness: str | int = None):

        # Stylesheet manager
        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'parent': parent,   'width': width,          'corner_roundness': corner_roundness, 'height': height,         'widget_color': widget_color},
                                  process_types     = {'parent': None,     'width': 'px-value;int', 'corner_roundness': 'px-value',       'height': 'px-value;int', 'widget_color': 'color'},
                                  default_values    = {'parent': None,     'width': '3 inch',       'corner_roundness': '0.03 inch',      'height': '2 inch',       'widget_color': 'cornflowerblue'},
                                  property_types    = {'parent': 'access', 'width': 'special',      'corner_roundness': 'stylesheet',     'height': 'special',      'widget_color': 'stylesheet'},
                                  special_functions = {'width': lambda v: self.set_size(v, self.height), 'height': lambda v: self.set_size(self.width, v)},
                                  base              = f"background-color: {V}widget_color{V}; border-radius: {V}corner_roundness{V};")

        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE

        self._widget = QFrame(parent._get_holder())
        self._widget.setStyleSheet(self._reloader.reload())

        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            parent._widget_box_add(self)
