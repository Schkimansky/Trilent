from PyQt6.QtWidgets import QFrame
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes
from trilent.FlexComputer import box


class Box(Misc):
    def __init__(self,
                 parent,
                 # Utility
                 alignment: str = None,
                 side_alignment: str = None,
                 width: int | str = None,
                 height: int | str = None,

                 # Styling
                 # Color
                 box_color: str = None,
                 # Fancy
                 corner_roundness: int | str = None,

                 # Flex Properties
                 wrap: bool = None,
                 gap: int | str = None,
                 vertical_gap: int | str = None):

        def width_func(v):
            self._widget.setGeometry(self.x, self.y, v, self.height)

        def height_func(v):
            self._widget.setGeometry(self.x, self.y, self.width, v)

        # Reloader setup
        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'parent': parent,   'width': width,          'height': height,         'box_color': box_color,     'corner_roundness': corner_roundness, 'alignment': alignment, 'side_alignment': side_alignment, 'wrap': wrap,     'gap': gap,            'vertical_gap': vertical_gap},
                                  process_types     = {'parent': None,     'width': 'px-value;int', 'height': 'px-value;int', 'box_color': 'color',       'corner_roundness': 'px-value',       'alignment': None,      'side_alignment': None,           'wrap': None,     'gap': 'px-value;int', 'vertical_gap': 'px-value;int'},
                                  default_values    = {'parent': None,     'width': '3 inch',       'height': '2 inch',       'box_color': 'transparent', 'corner_roundness': '0.03 inch',      'alignment': 'start',   'side_alignment': 'start',        'wrap': True,     'gap': '1 px',         'vertical_gap': '1 px'},
                                  property_types    = {'parent': 'access', 'width': 'special',      'height': 'special',      'box_color': 'stylesheet',  'corner_roundness': 'stylesheet',     'alignment': 'access',  'side_alignment': 'access',       'wrap': 'access', 'gap': 'access',       'vertical_gap': 'access'},
                                  special_functions = {'width': width_func, 'height': height_func},
                                  base              = f"background-color: {V}box_color{V}; border-radius: {V}corner_roundness{V}")

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.BOX
        self._dpi = parent.get_dpi()
        self._widgets = []
        self._children = []

        # Qt setup
        # noinspection PyProtectedMember
        self._widget = QFrame(self._reloader.cp['parent']._get_holder())
        self._reloader.cp['parent'].add_update_function(self._update)

        # Setup properties
        self._widget.setStyleSheet(self._reloader.reload())

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.cp['parent']._widget_box_add(self)

        self._update()

    def _get_holder(self): return self._widget

    def _widget_box_add(self, trilent_widget):
        self._children.append(trilent_widget)
        trilent_widget.force_place(0, 0)

    def _update(self):
        widths = tuple(child.width for child in self._children)
        heights = tuple(child.height for child in self._children)

        flex_args = (self._reloader.process(k, self._reloader.cp[k]) for k in ['alignment', 'side_alignment', 'wrap', 'gap', 'vertical_gap'])

        main_axis = box(widths, heights, self.width, self.height, *flex_args)

        for i, child in enumerate(self._children):
            child.set_position(main_axis[i][0], main_axis[i][1])

    def get_dpi(self): return self._dpi
    def add_update_function(self, f):
        self._reloader.cp['parent'].add_update_function(f)
