from typing import Any


class PropertyManager:
    def __init__(self, kwargs):
        self.properties = {}

        for name, value in kwargs.items():
            self.properties[name] = value

    def get_property(self, name) -> Any:
        return self.properties[name]

    def get_properties(self, *args) -> tuple[Any, ...]:
        return tuple(self.get_property(name) for name in args)

    def set_property(self, name, value):
        assert name in self.properties, ValueError(f'Invalid property name: {name}, Available properties are: {list(self.properties.keys())}')
        self.properties[name] = value

    def set_properties(self, **kwargs):
        for name, value in kwargs.items():
            self.set_property(name, value)

    def new_property(self, name, initial_value):
        assert name not in self.properties, ValueError(f'Property name already exists: {name}')
        self.properties[name] = initial_value

    def new_properties(self, **kwargs):
        for name, value in kwargs.items():
            self.new_property(name, value)

    def __getitem__(self, key):
        return self.get_property(key)

    def __setitem__(self, key, value):
        self.set_property(key, value)
