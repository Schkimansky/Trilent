from enum import Enum


V = '␟'


class WidgetStyleBase(Enum):
    WIDGET = f'background-color: {V}excess_color{V};'


class WidgetVarTypes(Enum):
    WIDGET = {'excess_color': 'color'}


class WidgetInitialValues(Enum):
    WIDGET = {'excess_color': 'transparent'}


class WidgetTypes(Enum):
    WIDGET = {'stylebase': WidgetStyleBase.WIDGET.value, 'var-types': WidgetVarTypes.WIDGET.value, 'initials': WidgetInitialValues.WIDGET.value}
