
def better_range(start_value, end_value):
    if start_value < end_value:
        return list(range(start_value, end_value + 1))
    elif start_value == end_value:
        return [end_value]
    elif start_value > end_value:
        return list(range(start_value, end_value, -1))


def break_px(string: str):
    """ Transforms '10px' to 10 """
    return int(float(string.removesuffix('px')))
