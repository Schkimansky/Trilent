from functools import lru_cache
from typing import Literal
from random import choice

colour_names = {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', 'aqua': '#00FFFF', 'aquamarine': '#7FFFD4', 'azure': '#F0FFFF', 'beige': '#F5F5DC', 'bisque': '#FFE4C4', 'black': '#000000', 'blanchedalmond': '#FFEBCD', 'blue': '#0000FF', 'blueviolet': '#8A2BE2', 'brown': '#A52A2A', 'burlywood': '#DEB887', 'cadetblue': '#5F9EA0', 'chartreuse': '#7FFF00', 'chocolate': '#D2691E', 'coral': '#FF7F50', 'cornflowerblue': '#6495ED', 'cornsilk': '#FFF8DC', 'crimson': '#DC143C', 'litecrimson': '#F21642', 'delightcrimson': '#D11339', 'cyan': '#00FFFF', 'darkblue': '#00008B', 'darkcyan': '#008B8B', 'darkgoldenrod': '#B8860B', 'darkgray': '#A9A9A9', 'darkgreen': '#006400', 'darkgrey': '#A9A9A9', 'darkkhaki': '#BDB76B', 'darkmagenta': '#8B008B', 'darkolivegreen': '#556B2F', 'darkorange': '#FF8C00', 'darkorchid': '#9932CC', 'darkred': '#8B0000', 'darksalmon': '#E9967A', 'darkseagreen': '#8FBC8F', 'darkslateblue': '#483D8B', 'darkslategray': '#2F4F4F', 'darkslategrey': '#2F4F4F', 'darkturquoise': '#00CED1', 'darkviolet': '#9400D3', 'deeppink': '#FF1493', 'deepskyblue': '#00BFFF', 'dimgray': '#696969', 'dimgrey': '#696969', 'dodgerblue': '#1E90FF', 'firebrick': '#B22222', 'floralwhite': '#FFFAF0', 'forestgreen': '#228B22', 'fuchsia': '#FF00FF', 'gainsboro': '#DCDCDC', 'ghostwhite': '#F8F8FF', 'gold': '#FFD700', 'goldenrod': '#DAA520', 'gray': '#808080', 'green': '#008000', 'greenyellow': '#ADFF2F', 'grey': '#808080', 'honeydew': '#F0FFF0', 'hotpink': '#FF69B4', 'indianred': '#CD5C5C', 'indigo': '#4B0082', 'ivory': '#FFFFF0', 'khaki': '#F0E68C', 'lavender': '#E6E6FA', 'lavenderblush': '#FFF0F5', 'lawngreen': '#7CFC00', 'lemonchiffon': '#FFFACD', 'lightblue': '#ADD8E6', 'lightcoral': '#F08080', 'lightcyan': '#E0FFFF', 'lightgoldenrodyellow': '#FAFAD2', 'lightgray': '#D3D3D3', 'lightgreen': '#90EE90', 'lightgrey': '#D3D3D3', 'lightpink': '#FFB6C1', 'lightsalmon': '#FFA07A', 'lightseagreen': '#20B2AA', 'lightskyblue': '#87CEFA', 'lightslategray': '#778899', 'lightslategrey': '#778899', 'lightsteelblue': '#B0C4DE', 'lightyellow': '#FFFFE0', 'lime': '#00FF00', 'limegreen': '#32CD32', 'linen': '#FAF0E6', 'magenta': '#FF00FF', 'maroon': '#800000', 'mediumaquamarine': '#66CDAA', 'mediumblue': '#0000CD', 'mediumorchid': '#BA55D3', 'mediumpurple': '#9370DB', 'mediumseagreen': '#3CB371', 'mediumslateblue': '#7B68EE', 'mediumspringgreen': '#00FA9A', 'mediumturquoise': '#48D1CC', 'mediumvioletred': '#C71585', 'midnightblue': '#191970', 'mintcream': '#F5FFFA', 'mistyrose': '#FFE4E1', 'moccasin': '#FFE4B5', 'navajowhite': '#FFDEAD', 'navy': '#000080', 'oldlace': '#FDF5E6', 'olive': '#808000', 'olivedrab': '#6B8E23', 'orange': '#FFA500', 'orangered': '#FF4500', 'orchid': '#DA70D6', 'palegoldenrod': '#EEE8AA', 'palegreen': '#98FB98', 'paleturquoise': '#AFEEEE', 'palevioletred': '#DB7093', 'papayawhip': '#FFEFD5', 'peachpuff': '#FFDAB9', 'peru': '#CD853F', 'pink': '#FFC0CB', 'plum': '#DDA0DD', 'powderblue': '#B0E0E6', 'purple': '#800080', 'red': '#FF0000', 'rosybrown': '#BC8F8F', 'royalblue': '#4169E1', 'saddlebrown': '#8B4513', 'salmon': '#FA8072', 'sandybrown': '#F4A460', 'seagreen': '#2E8B57', 'seashell': '#FFF5EE', 'sienna': '#A0522D', 'silver': '#C0C0C0', 'skyblue': '#87CEEB', 'slateblue': '#6A5ACD', 'slategray': '#708090', 'slategrey': '#708090', 'snow': '#FFFAFA', 'springgreen': '#00FF7F', 'steelblue': '#4682B4', 'tan': '#D2B48C', 'teal': '#008080', 'thistle': '#D8BFD8', 'tomato': '#FF6347', 'turquoise': '#40E0D0', 'violet': '#EE82EE', 'wheat': '#F5DEB3', 'white': '#FFFFFF', 'whitesmoke': '#F5F5F5', 'yellow': '#FFFF00', 'yellowgreen': '#9ACD32', 'xylon': '#0074D9'}
rect_definings = {'horizontal': 'x1: 0, y1: 0, x2: 1, y2: 0',
                  'vertical': 'x1: 0, y1: 0, x2: 0, y2: 1',
                  'diagonal': 'x1: 0, y1: 0, x2: 1, y2: 1',
                  'inverted diagonal': 'x1: 1, y1: 0, x2: 0, y2: 1'}


@lru_cache
def get_hex_colour(string):
    name = string.lower()
    return colour_names[name]


def convert_gradient(value):
    direction: Literal['horizontal', 'vertical', 'diagonal', 'inverted diagonal'] = 'horizontal'
    colors = value.split(' -> ')

    if value.__contains__(' | '):
        direction = value.split(' | ')[-1]
        colors = value.split(' | ')[0].split(' -> ')

    qt_string = f"qlineargradient({rect_definings[direction]}, "

    each_color_increment = 1 / (len(colors) - 1)

    for i, color in enumerate(colors):
        qt_string += f'stop: {each_color_increment * i} {get_as_qt(color)}{', ' if i + 1 != len(colors) else ''}'

    return qt_string + ')'


@lru_cache
def get_color_type(value: str):
    if value == 'transparent':
        color_type = 'special'
    elif value == 'random':
        value = choice(list(colour_names.keys()))
        color_type = 'hex'
    elif value.count('->'):
        color_type = 'gradient'
    elif value.startswith('#') and len(value) == 7:  # 7 because it includes "#"
        color_type = 'hex'
    elif value.startswith('#') and len(value) > 7:
        color_type = 'long-hex'
    elif value.count(',') == 2:
        color_type = 'rgb'
    elif value.count(',') > 2:
        color_type = 'long-rgb'
    else:
        color_type = 'hex'
        value = get_hex_colour(value)
    return value, color_type


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


def hexa_to_rgba(hexa):
    r = int(hexa[1:3], 16)
    g = int(hexa[3:5], 16)
    b = int(hexa[5:7], 16)
    a = int(hexa[7:9], 16)
    return f'rgba({r}, {g}, {b}, {a})'


def get_as_qt(value):
    value, color_type = get_color_type(value)

    if color_type == 'special':
        return 'transparent'
    elif color_type == 'hex':
        return value
    elif color_type == 'long-hex':
        return hexa_to_rgba(value)
    elif color_type == 'rgb':
        split = value.split(',')
        return f'rgb({split[0]},{split[1]},{split[2]})'
    elif color_type == 'long-rgb':
        split = value.split(',')
        return f'rgba({split[0]},{split[1]},{split[2]},{split[3]})'
    elif color_type == 'gradient':
        return convert_gradient(value)

    raise ValueError(f'Invalid color type: {value}')


def get_as_raw_qt(value):
    value, color_type = get_color_type(value)

    if color_type == 'special':
        return (0, 0, 0, 0)
    elif color_type == 'hex':
        return convert_hex_to_rgba(value)
    elif color_type == 'long-hex':
        return convert_hex_to_rgba(value)
    elif color_type == 'rgb':
        split = value.split(',')
        return split + [255]
    elif color_type == 'long-rgb':
        return value.split(',')
    elif color_type == 'gradient':
        raise NotImplementedError('Raw conversion for gradients isnt supported yet.')

    raise ValueError(f'Invalid color type: {value}')
