from conversa import distance
from functools import lru_cache

trilent_to_conversa = {'inch': 'inches'}


@lru_cache
def get_in_pixels(value: str | int, dpi: int) -> int:
    if isinstance(value, int):
        return value  # Already in px

    value, unit = value.split(' ')
    if unit == 'px':
        return value  # Again, already in px
    else:
        unit_in_inches = int(distance(float(value), trilent_to_conversa[unit], 'inches'))
        return unit_in_inches * dpi
