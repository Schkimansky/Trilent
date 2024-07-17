from .color import get_as_qt
from .unit import get_in_pixels
from .orientation import qt_orientation
from typing import Any, Literal


V = '␟'


class Reloader:
    def __init__(self, dpi: int,
                 setup_properties: dict[str, Any],
                 process_types: dict[str, str],
                 default_values: dict[str, Any],
                 property_types: dict[str, Literal['stylesheet', 'special', 'access']],
                 special_functions: dict[str, Any],
                 base: str):
        self.initial_parameters = {'setup_properties': setup_properties,
                                   'process_types': process_types,
                                   'default_values': default_values,
                                   'property_types': property_types,
                                   'special_functions': special_functions,
                                   'base': base}

        self.dpi = dpi
        self.property_types = property_types
        self.all_properties = list(setup_properties.keys())
        self.base = base

        self.process_types = process_types
        self.special_functions = special_functions

        self.cp = {}

        for p, v in setup_properties.items():
            self.cp[p] = default_values[p] if v is None else v

    def process(self, property_name: str, value: str):
        match self.process_types[property_name]:
            case 'color':
                return str(get_as_qt(value))
            case 'px-value':
                return str(get_in_pixels(value, self.dpi)) + 'px'
            case 'raw':
                return str(value)
            case 'px-value;int':
                return int(get_in_pixels(value, self.dpi))
            case 'orientation':
                return qt_orientation(value)
            case 'super raw':
                return value
            case None:
                return value

    def alternate_process(self, property_name: str, value: str):
        match property_name:
            case 'color':
                return str(get_as_qt(value))
            case 'px-value':
                return str(get_in_pixels(value, self.dpi)) + 'px'
            case 'raw':
                return str(value)
            case 'px-value;int':
                return int(get_in_pixels(value, self.dpi))
            case 'orientation':
                return qt_orientation(value)
            case 'super raw':
                return value
            case None:
                return value

    def reload(self):
        base = self.base

        for p, v in self.cp.items():
            if self.property_types[p] == 'special':
                self.special_functions[p](self.process(p, v))
            elif self.property_types[p] == 'stylesheet':
                base = base.replace(f"{V}{p}{V}", self.process(p, v))

        return base

    def set(self, p, v):
        if self.process_types[p] == 'special':
            self.special_functions[p](self.process(p, v))
        else:
            self.cp[p] = v

    def get(self, p):
        return self.cp[p]


def bench():
    for i in range(500):
        reloader.reload()


if __name__ == '__main__':
    reloader = Reloader(92,
                              {'parent': None, 'width': None, 'height': None, 'background_color': None,
                               'corner_roundness': None, 'alignment': None,
                               'side_alignment': None, 'wrap': None, 'gap': None,
                               'vertical_gap': None},
                              {'parent': None, 'width': 'px-value;int', 'height': 'px-value;int',
                               'background_color': 'color', 'corner_roundness': 'px-value', 'alignment': None,
                               'side_alignment': None, 'wrap': None, 'gap': 'px-value;int',
                               'vertical_gap': 'px-value;int'},
                              {'parent': None, 'width': '3 inch', 'height': '2 inch',
                               'background_color': 'cornflowerblue', 'corner_roundness': '10 px', 'alignment': 'start',
                               'side_alignment': 'start', 'wrap': True, 'gap': '1 px', 'vertical_gap': '1 px'},
                              {'parent': 'access', 'width': 'special', 'height': 'special',
                               'background_color': 'stylesheet', 'corner_roundness': 'stylesheet',
                               'alignment': 'access', 'side_alignment': 'access', 'wrap': 'access', 'gap': 'access',
                               'vertical_gap': 'access'},
                              {'width': lambda v: 0, 'height': lambda v: 0},
                              f"background-color: {V}background_color{V}; border-radius: {V}corner_roundness{V}")

    import cProfile
    cProfile.run('bench()')
