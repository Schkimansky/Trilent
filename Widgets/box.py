from PyQt5.QtWidgets import QFrame
from Trilent.Utility import get_in_pixels, Reloader, WidgetTypes
from Trilent.Widgets import PositionTypes
from Trilent.Widgets.widget import Widget
from Trilent.FlexComputer import box


class Box(Widget):
    def __init__(self,
                 parent,
                 # Utility
                 width: int | str = '3 inch',        # Semi Function
                 height: int | str = '2 inch',       # Semi Function

                 # Styling
                 # Color
                 background_color=None,         # Needs Reload (QML, Slow)
                 excess_color: str = None,  # Needs Reload (PQML, Slow)
                 # Fancy
                 corner_roundness: int | str = None,

                 # Flex Properties
                 alignment: str = 'start',
                 side_alignment: str = 'start',
                 wrap: bool = True,
                 gap: int = 5,
                 vertical_gap: int = 5):

        super().__init__(parent, width, height, excess_color=excess_color)

        # Reloader setup
        self._reloader = Reloader(WidgetTypes.BOX, self.get_dpi(),

                                  alignment=alignment,
                                  side_alignment=side_alignment,
                                  wrap=wrap,
                                  gap=gap,
                                  vertical_gap=vertical_gap,
                                  background_color=background_color,
                                  parent=parent,
                                  width=width,
                                  height=height,
                                  corner_roundness=corner_roundness,
                                  excess_color=excess_color)

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.properties['parent']._position_children
        self._position_children = PositionTypes.BOX
        self._dpi = parent.get_dpi()
        self._widgets = []
        self._children = []

        # Qt setup
        # noinspection PyProtectedMember
        self._frame = QFrame(self._reloader.properties['parent']._get_holder())
        self._reloader.properties['parent'].add_update_function(self._update)

        # Setup properties
        self._reloader.reload_start()
        self._frame.setStyleSheet(self._reloader.stylesheet)

        self._frame.setGeometry(0, 0, get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.properties['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.properties['parent']._widget_box_add(self)

    def set_size(self, width, height):
        self._frame.setGeometry(self.x, self.y, width, height)
        super().set_size(width, height)
        self._reloader.properties.set_property('width', width)
        self._reloader.properties.set_property('height', height)

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

        main_axis = box(widths, heights, self.width, self.height, wrap=self._reloader.properties['wrap'],
                        alignment=self._reloader.properties['alignment'],
                        side_alignment=self._reloader.properties['side_alignment'],
                        gap=self._reloader.properties['gap'], vertical_gap=self._reloader.properties['vertical_gap'])
        [child.set_position(main_axis[i][0], main_axis[i][1]) for i, child in enumerate(self._children)]

    def set(self, property_name, value):
        self._reloader.properties[property_name] = value

        if property_name == 'excess_color':
            super().set(property_name, value)
        else:
            self._reloader.reload(property_name, value)
            self._frame.setStyleSheet(self._reloader.stylesheet)

    def get(self, property_name):
        return self._reloader.properties[property_name]
