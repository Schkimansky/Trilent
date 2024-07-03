from PyQt6.QtWidgets import QFrame
from Trilent.Utility import Reloader, V, Misc, PositionTypes


class Widget(Misc):
    def __init__(self,
                 parent,
                 width: int | str,
                 height: int | str,
                 excess_color: str = None):

        # Stylesheet manager
        self._reloader = Reloader(parent.get_dpi(),
                                  {'parent': parent, 'width': width,          'height': height,         'excess_color': excess_color},
                                  {'parent': None,   'width': 'px-value;int', 'height': 'px-value;int', 'excess_color': 'color'},
                                  {'parent': None,   'width': '3 inch',       'height': '2 inch',       'excess_color': 'transparent'},
                                  {'parent': 'access', 'width': 'special',   'height': 'special',      'excess_color': 'stylesheet'},
                                  {'width': lambda v: self.set_size(v, self.height), 'height': lambda v: self.set_size(self.width, v)},
                                  f"background-color: {V}excess_color{V};")

        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE

        self._widget = QFrame(parent._get_holder())
        self._widget.setStyleSheet(self._reloader.reload())

        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            parent._widget_box_add(self)
