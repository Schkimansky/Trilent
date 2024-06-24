from .color import get_as_qt
from .unit import get_in_pixels
from .qss_styles import WidgetTypes, V
from .property_manager import PropertyManager


class Reloader:
    def __init__(self, widget_type: WidgetTypes, dpi: int, **kwargs):
        self.dpi = dpi

        self.properties = PropertyManager(kwargs)

        self.widget_type      = widget_type
        self.var_types        = self.widget_type.value['var-types']
        self.i = self.widget_type.value['initials'].copy()

        self.stylesheet = widget_type.value['stylebase']

        for kw, v in kwargs.items():
            if kw in self.var_types:
                # Set any defining parameters set
                if v is not None:
                    self.i[kw] = v

        self.changed_initials = self.i

        for k, v in self.i.items():
            self.stylesheet = self.stylesheet.replace(f'{V}{k}{V}', self.qss_value(k, v))

    def reload(self, property_name, property_value):
        self.changed_initials[property_name] = self.qss_value(property_name, property_value)
        self.properties[property_name] = property_value

        # Reload stylesheet to the starting point
        self.stylesheet = self.widget_type.value['stylebase']

        for k, v in self.changed_initials.items():
            # Replace variables with their changed values
            self.stylesheet = self.stylesheet.replace(f'{V}{k}{V}', self.qss_value(k, v))

    def reload_start(self):
        # Reload stylesheet to the starting point
        self.stylesheet = self.widget_type.value['stylebase']

        for k, v in self.changed_initials.items():
            # Replace variables with their changed values
            self.stylesheet = self.stylesheet.replace(f'{V}{k}{V}', self.qss_value(k, v))

    def qss_value(self, property_name: str, value: str):
        if self.var_types[property_name] == 'color':
            return get_as_qt(value)
        elif self.var_types[property_name] == 'px-value':
            return str(get_in_pixels(value, self.dpi)) + 'px'
        elif self.var_types[property_name] == 'raw':
            return str(value)

    @property
    def qss_stylesheet(self):
        return self.stylesheet


if __name__ == '__main__':
    reloader = Reloader(WidgetTypes.WIDGET, 92)

    reloader.reload('excess_color', 'transparent')

    print(reloader.stylesheet)
