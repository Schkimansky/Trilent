from PyQt6.QtWidgets import QFrame
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes


class Frame(Misc):
    def __init__(self,
                 parent,
                 # Utility
                 width: int | str = None,
                 height: int | str = None,

                 # Styling
                 # Color
                 frame_color: str = None,
                 # Fancy
                 corner_roundness: int | str = None):

        def width_func(v): self._widget.setGeometry(self.x, self.y, v, self.height)
        def height_func(v): self._widget.setGeometry(self.x, self.y, self.width, v)

        # Reloader setup
        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'parent': parent,   'width': width,          'height': height,         'frame_color': frame_color,      'corner_roundness': corner_roundness},
                                  process_types     = {'parent': None,     'width': 'px-value;int', 'height': 'px-value;int', 'frame_color': 'color',          'corner_roundness': 'px-value'},
                                  default_values    = {'parent': None,     'width': '3 inch',       'height': '2 inch',       'frame_color': '255,255,255,30', 'corner_roundness': '0.03 inch'},
                                  property_types    = {'parent': 'access', 'width': 'special',      'height': 'special',      'frame_color': 'stylesheet',     'corner_roundness': 'stylesheet'},
                                  special_functions = {'width': width_func, 'height': height_func},
                                  base              = f"background-color: {V}frame_color{V}; border-radius: {V}corner_roundness{V}")

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.PLACE
        self._dpi = parent.get_dpi()

        # Qt setup
        # noinspection PyProtectedMember
        self._widget = QFrame(self._reloader.cp['parent']._get_holder())

        # Setup properties
        self._widget.setStyleSheet(self._reloader.reload())

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)

    def _get_holder(self): return self._widget

    def get_dpi(self): return self._dpi
