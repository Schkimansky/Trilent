from functools import lru_cache
import multiprocessing
from typing import List
from .color import get_as_qt


def split_rgb_format(rgb_string: str):
    color_channels = [int(channel) for channel in
                      rgb_string.removeprefix('rgb(').removeprefix('rgba(')[:-1].split(', ')]

    if len(color_channels) == 3:
        color_channels.append(255)

    return color_channels


def convert_hex_to_rgba(hex_color: str) -> list[int]:
    if hex_color.startswith('rgb(') or hex_color.startswith('rgba('):
        return split_rgb_format(hex_color)

    hex_color = f"{hex_color[1:]}FF"

    rgba = [int((hex_color + 'FF')[0:2], 16),
            int((hex_color + 'FF')[2:4], 16),
            int((hex_color + 'FF')[4:6], 16),
            int((hex_color + 'FF')[6:8], 16)]

    return rgba


def convert_rgba_to_hex(r, g, b, a=255) -> str: return f'#{r:02x}{g:02x}{b:02x}{a:02x}'


@lru_cache(30)
def color_gradient(color1: str | tuple[int, int, int], color2: str | tuple[int, int, int], steps: int = 10) -> list[
    str]:
    color1 = convert_hex_to_rgba(color1)
    color2 = convert_hex_to_rgba(color2)

    steps -= 1

    step_r = (color2[0] - color1[0]) / steps
    step_g = (color2[1] - color1[1]) / steps
    step_b = (color2[2] - color1[2]) / steps
    step_a = (color2[3] - color1[3]) / steps

    gradient = [
        convert_rgba_to_hex(int(color1[0] + step_r * i), int(color1[1] + step_g * i), int(color1[2] + step_b * i),
                            int(color1[3] + step_a * i)) for i in range(steps + 1)]

    return gradient


def multi_color_gradient(colors: list[str | tuple[int, int, int, int]], steps: int = 10) -> list[str]:
    gradient = []
    num_colors = len(colors)

    for i in range(num_colors - 1):
        color1 = convert_hex_to_rgba(colors[i])
        color2 = convert_hex_to_rgba(colors[i + 1])

        steps_between = steps - 1

        step_r = (color2[0] - color1[0]) / steps_between
        step_g = (color2[1] - color1[1]) / steps_between
        step_b = (color2[2] - color1[2]) / steps_between
        step_a = (color2[3] - color1[3]) / steps_between

        for j in range(steps_between):
            r = int(color1[0] + step_r * j)
            g = int(color1[1] + step_g * j)
            b = int(color1[2] + step_b * j)
            a = int(color1[3] + step_a * j)
            gradient.append(convert_rgba_to_hex(r, g, b, a))

        gradient.append(convert_rgba_to_hex(*color2))

    return gradient


def blend_color(color1: str, color2: str, step_ratio: float) -> str:
    c1 = convert_hex_to_rgba(color1)
    c2 = convert_hex_to_rgba(color2)
    blended_color = (int(c1[0] * (1 - step_ratio) + c2[0] * step_ratio),
                     int(c1[1] * (1 - step_ratio) + c2[1] * step_ratio),
                     int(c1[2] * (1 - step_ratio) + c2[2] * step_ratio),
                     int(c1[3] * (1 - step_ratio) + c2[3] * step_ratio))
    return convert_rgba_to_hex(blended_color[0], blended_color[1], blended_color[2], blended_color[3])


def blend_gradient_step(step: int, grad1: List[str], grad2: List[str], steps: int) -> str:
    step_ratio = step / steps
    blended_colors = [blend_color(color1, color2, step_ratio) for color1, color2 in zip(grad1, grad2)]
    return " -> ".join(blended_colors)


def blend_gradients(grad1: List[str], grad2: List[str], steps: int) -> List[str]:
    with multiprocessing.Pool() as pool:
        tasks = [(i, grad1, grad2, steps) for i in range(steps + 1)]
        blended_gradients = pool.starmap(blend_gradient_step, tasks)
    return blended_gradients


def gradient_gradient(gradient1: str, gradient2: str, steps: int, color_steps: int) -> list[str]:
    gradient1_colors = [get_as_qt(color) for color in gradient1.split(' -> ')]
    gradient2_colors = [get_as_qt(color) for color in gradient2.split(' -> ')]

    grad1 = multi_color_gradient(gradient1_colors, color_steps)
    grad2 = multi_color_gradient(gradient2_colors, color_steps)

    result = blend_gradients(grad1, grad2, steps)

    return result
