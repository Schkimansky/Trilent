from color import get_as_qt
from unit import get_in_pixels
from qss_styles import WidgetTypes, V, WidgetVarTypes, WidgetInitialValues


class Reloader:
    def __init__(self, widget_ptr, widget_type: WidgetTypes, dpi: int):
        self.dpi = dpi

        self.widget           = widget_ptr
        self.widget_type      = widget_type
        self.var_types        = self.widget_type.value['var-types']
        self.changed_initials = self.widget_type.value['initials']

        self.stylesheet = widget_type.value['stylebase']

        for k, v in self.widget_type.value['initials'].items():
            self.stylesheet = self.stylesheet.replace(f'{V}{k}{V}', self.qss_value(k, v))

    def reload(self, property_name, property_value):
        self.changed_initials[property_name] = self.qss_value(property_name, property_value)
        # Reload stylesheet to the starting point
        self.stylesheet = self.widget_type.value['stylebase']

        for k, v in self.changed_initials.items():
            # Replace variables with their changed values
            self.stylesheet = self.stylesheet.replace(f'{V}{k}{V}', self.qss_value(k, v))

    def qss_value(self, property_name: str, value: str):
        if self.var_types[property_name] == 'color':
            return get_as_qt(value)
        elif self.var_types[property_name] == 'px-value':
            return str(get_in_pixels(value, self.dpi))

    @property
    def qss_stylesheet(self):
        return self.stylesheet


def index_end_of(string, substring):
    substring_length = len(substring)

    for i in range(len(string)):
        if string[i:i + substring_length] == substring:
            return i, i + substring_length


def index_replace(string, substring, si, ei):
    return string[:si] + substring + string[ei:]


if __name__ == '__main__':
    reloader = Reloader(1, WidgetTypes.WIDGET, 92)

    reloader.reload('excess_color', 'transparent')

    print(reloader.stylesheet)
