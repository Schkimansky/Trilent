from functools import lru_cache


def convert_hex_to_rgba(hex_color: str) -> list[int]:
    if hex_color.startswith('rgb(') or hex_color.startswith('rgba('):
        return split_rgb_format(hex_color)

    hex_color += 'FF'

    return list(int((hex_color + 'FF').removeprefix('#')[i:i + 2], 16) for i in (0, 2, 4, 6))


def convert_rgb_to_hex(r, g, b, a=255) -> str:
    return '#{:02x}{:02x}{:02x}{:02x}'.format(r, g, b, a)


def split_rgb_format(rgb_string: str):
    color_channels = [int(channel) for channel in rgb_string.removeprefix('rgb(').removeprefix('rgba(')[:-1].split(', ')]

    if len(color_channels) == 3:
        color_channels.append(255)

    return color_channels


@lru_cache(30)
def gradient_list(color1: str | tuple[int, int, int], color2: str | tuple[int, int, int], steps: int = 10) -> list[str]:
    color1 = convert_hex_to_rgba(color1) if isinstance(color1, str) else color1
    color2 = convert_hex_to_rgba(color2) if isinstance(color2, str) else color2

    steps -= 1

    step_r = (color2[0] - color1[0]) / steps
    step_g = (color2[1] - color1[1]) / steps
    step_b = (color2[2] - color1[2]) / steps
    step_a = (color2[3] - color1[3]) / steps

    gradient = [convert_rgb_to_hex(int(color1[0] + step_r * i), int(color1[1] + step_g * i), int(color1[2] + step_b * i), int(color1[3] + step_a * i)) for i in range(steps + 1)]

    return gradient


def bench():
    gradient = gradient_list('#FF0000', '#0000FF', steps=255)

    print(gradient)


if __name__ == '__main__':
    import cProfile
    cProfile.run('bench()')
