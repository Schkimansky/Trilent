from conversa import distance
from PyQt5.Qt import QApplication
from sys import argv
from functools import lru_cache


@lru_cache
def get_dpi():
    app = QApplication(argv)
    desktop = app.desktop()
    result = desktop.logicalDpiX()
    app.quit()

    return result


dpi = get_dpi()
trilent_to_conversa = {'inch': 'inches'}


class Unit:
    def __init__(self, value: str):
        self.value = value

    def get_in_pixels(self):
        return get_in_pixels(self.value)


@lru_cache
def get_in_pixels(value: str | int) -> int:
    if isinstance(value, int):
        return value  # Already in px

    value, unit = value.split(' ')
    if unit == 'px':
        return value  # Again, already in px
    else:
        unit_in_inches = int(distance(float(value), trilent_to_conversa[unit], 'inches'))
        return unit_in_inches * dpi

