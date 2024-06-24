from PyQt5.QtWidgets import QLabel
from Trilent.Utility import get_in_pixels, Reloader, WidgetTypes, qt_orientation
from Trilent.Widgets import PositionTypes
from Trilent.Widgets.widget import Widget


class Text(Widget):
    def __init__(self,
                 parent,
                 # Widget specific, Property included
                 text: str = 'Trilent label.',
                 orientation: str = 'top left',
                 text_size: str | int = '10 px',
                 font: str = 'Arial',
                 # Utility
                 width: int | str = '3 inch',
                 height: int | str = '2 inch',
                 auto_size: bool = True,  # Controls if you dont wanna enter width and height
                 # Styling
                 # Color
                 background_color: str = None,
                 excess_color: str = None,
                 text_color: str = None,
                 # Fancy
                 corner_roundness: int | str = None):

        super().__init__(parent, width, height, excess_color=excess_color)

        # Reloader setup
        self._reloader = Reloader(WidgetTypes.TEXT, self.get_dpi(),
                                  text=text,
                                  text_color=text_color,
                                  background_color=background_color,
                                  parent=parent,
                                  width=width,
                                  height=height,
                                  corner_roundness=corner_roundness,
                                  excess_color=excess_color,
                                  orientation=orientation,
                                  text_size=text_size,
                                  font=font,
                                  auto_size=auto_size)
        self._reloader.reload_start()

        # Protected widget specific members
        # noinspection PyProtectedMember
        self._position_self = self._reloader.properties['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        # noinspection PyProtectedMember
        self._widget = QLabel(self._reloader.properties['text'], self._reloader.properties['parent']._get_holder())
        self._widget.setAlignment(qt_orientation(self._reloader.properties['orientation']))

        # Setup properties
        self._widget.setStyleSheet(self._reloader.stylesheet)
        self._widget.setGeometry(0, 0, get_in_pixels(width, self._dpi), get_in_pixels(height, self._dpi))

        # Check if Box's parent is also a box
        # noinspection PyProtectedMember
        if self._reloader.properties['parent']._position_children == PositionTypes.BOX:
            # noinspection PyProtectedMember
            self._reloader.properties['parent']._widget_box_add(self)

        if self._reloader.properties['auto_size'] is True:
            self._widget.adjustSize()

    def set_size(self, width, height):
        self._widget.setGeometry(self.x, self.y, width, height)
        super().set_size(width, height)
        self._reloader.properties.set_property('width', width)
        self._reloader.properties.set_property('height', height)

    def show(self): self._widget.show()
    def hide(self): self._widget.hide()

    def _get_holder(self):
        return self._widget

    def set(self, property_name, value):
        self._reloader.properties[property_name] = value

        if property_name == 'excess_color':
            super().set(property_name, value)
        # Special widget specific properties.
        elif property_name == 'text':
            self._reloader.properties[property_name] = value
            self._widget.setText(value)
            if self._reloader.properties['auto_size'] is True:
                self._widget.adjustSize()
        elif property_name == 'orientation':
            self._widget.setAlignment(qt_orientation(self._reloader.properties['orientation']))
        else:
            self._reloader.reload(property_name, value)
            self._widget.setStyleSheet(self._reloader.stylesheet)

    def get(self, property_name):
        return self._reloader.properties[property_name]
