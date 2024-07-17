from conversa import distance
from functools import lru_cache

trilent_to_conversa = {'inch': 'inches'}


@lru_cache
def get_in_pixels(value: str | int, dpi: int) -> int | float:
    if isinstance(value, int) or isinstance(value, float):
        return value  # Already in px

    value, unit = value.split(' ')[0], value.split(' ')[1] if len(value.split(' ')) == 2 else 'px'

    if unit == 'px':
        return float(value)  # Again, already in px
    else:
        unit_in_inches = distance(float(value), trilent_to_conversa[unit], 'inches')
        return int(unit_in_inches * dpi)
