from enum import Enum


V = '␟'


class WidgetStyleBase(Enum):
    WIDGET = f'background-color: {V}excess_color{V};'
    BOX = f'background-color: {V}background_color{V}; border-radius: {V}corner_roundness{V};'
    TEXT = f'color: {V}text_color{V}; background-color: {V}background_color{V}; border-radius: {V}corner_roundness{V}; font-family: {V}font{V}; font-size: {V}text_size{V};'


class WidgetVarTypes(Enum):
    WIDGET = {'excess_color': 'color'}
    BOX    = {'background_color': 'color', 'corner_roundness': 'px-value'}
    TEXT   = {'text_color': 'color', 'background_color': 'color', 'corner_roundness': 'px-value', 'font': 'raw', 'text_size': 'px-value'}


class WidgetInitialValues(Enum):
    WIDGET = {'excess_color': 'transparent'}
    BOX    = {'background_color': '#242424', 'corner_roundness': '0.08 inch'}
    TEXT   = {'text_color': 'white', 'background_color': 'transparent', 'corner_roundness': '0 px', 'font': 'Arial', 'text_size': '0.3 inch'}


class WidgetTypes(Enum):
    WIDGET = {'stylebase': WidgetStyleBase.WIDGET.value, 'var-types': WidgetVarTypes.WIDGET.value, 'initials': WidgetInitialValues.WIDGET.value}
    BOX    = {'stylebase': WidgetStyleBase.BOX.value, 'var-types': WidgetVarTypes.BOX.value, 'initials': WidgetInitialValues.BOX.value}
    TEXT   = {'stylebase': WidgetStyleBase.TEXT.value, 'var-types': WidgetVarTypes.TEXT.value, 'initials': WidgetInitialValues.TEXT.value}
