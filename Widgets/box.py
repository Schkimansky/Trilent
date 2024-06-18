from PyQt5.QtWidgets import QFrame
from Trilent.Utility import get_in_pixels, get_as_qt
from Trilent.Widgets import PositionTypes
from Trilent.Widgets.widget import Widget
from Trilent.FlexComputer import box
from Trilent.Utility import PropertyManager


class Box(Widget):
    def __init__(self,
                 parent,
                 # Utility
                 width: int | str = '3 inch',
                 height: int | str = '2 inch',
                 # Color
                 background_color='#303030',
                 # Flex Properties
                 alignment: str = 'start',
                 side_alignment: str = 'start',
                 wrap: bool = True,
                 gap: int = 5,
                 vertical_gap: int = 5,
                 excess_color: str = 'transparent'):

        super().__init__(parent, width, height, excess_color=excess_color)

        # Properties setup
        self._properties = PropertyManager(alignment=alignment,
                                           side_alignment=side_alignment,
                                           wrap=wrap,
                                           gap=gap,
                                           vertical_gap=vertical_gap,
                                           background_color=background_color,
                                           width=width,
                                           height=height,
                                           parent=parent)

        # Protected widget specific members
        self._positionType = PositionTypes.BOX
        self._dpi = parent.get_dpi()
        self._widgets = []
        self._children = []

        # Qt setup
        self._frame = QFrame(self._properties['parent']._get_holder())
        self._properties['parent'].add_update_function(self._update)

        # Setup properties
        self._frame.setStyleSheet(f"background-color: {get_as_qt(background_color)};")
        self._frame.setGeometry(0, 0, get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

        # Check if Box's parent is also a box
        if self._properties['parent']._positionType == PositionTypes.BOX:
            self._properties['parent']._widget_box_add(self)

    def place(self, x: int = 100, y: int = 100):
        assert self._positionType == PositionTypes.BOX, TypeError("You cant place a widget whose parent is a box.")

        geometry = self._frame.geometry()
        self._frame.setGeometry(x, y, geometry.width(), geometry.height())
        self._frame.show()

    def set_position(self, x, y): self._frame.setGeometry(x, y, self.width, self.height)
    def set_size(self, width, height): self._frame.setGeometry(self.x, self.y, width, height)

    def show(self): self._frame.show()
    def hide(self): self._frame.hide()

    def _get_holder(self):
        return self._frame

    def _widget_box_add(self, trilent_widget):
        self._children.append(trilent_widget)
        trilent_widget.force_place(0, 0)

    def _update(self):
        widths = tuple(child.width for child in self._children)
        heights = tuple(child.height for child in self._children)

        main_axis = box(widths, heights, self.width, self.height, wrap=self._properties['wrap'], alignment=self._properties['alignment'], side_alignment=self._properties['side_alignment'], gap=self._properties['gap'], vertical_gap=self._properties['vertical_gap'])
        [child.set_position(main_axis[i][0], main_axis[i][1]) for i, child in enumerate(self._children)]

    def get_dpi(self): return self._properties['parent'].get_dpi()

    def set(self, property_name, value):
        self._properties[property_name] = value

        if property_name == 'background_color':
            self._frame.setStyleSheet(f"background-color: {get_as_qt(self._properties['background_color'])};")

    def get(self, property_name):
        return self._properties[property_name]
