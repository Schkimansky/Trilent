from trilent.Utility.color_gradients import color_gradient, gradient_gradient
from trilent.Utility.other_gradients import text_gradient
from .helpers import better_range, break_px
from typing import Any


def generate_lists(name: str, type: str, start_value: Any, end_value: Any, mode: str = "") -> list:
    if type == 'px-value;int':
        # No need to break them up, Since it comes processed as ints.
        return better_range(start_value, end_value)
    elif type == 'px-value':
        # Break up the strings using break px,
        # Because the values often come processed as strings.
        return better_range(break_px(start_value), break_px(end_value))
    elif type == 'gradient color':
        # The more the steps/color_steps, The more the calculation times.
        return gradient_gradient(start_value, end_value, 200, 30)
    elif type == 'color':
        return color_gradient(start_value, end_value, 255)
    elif type == 'text':
        return text_gradient(start_value, end_value, mode)
    else:
        raise NotImplementedError(f'Animations for "{name}" isn\'t supported yet. Type: {type}')
