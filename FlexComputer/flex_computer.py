from functools import lru_cache


def calculate_start_positions(widths: tuple[int, ...], heights: tuple[int, ...],
                              side_alignment: str,
                              flex_box_size: tuple[int | str, int | str],
                              wrap: bool, gap: int, vertical_gap: int) -> list[list[int]]:
    """ This function calculates the starting positions for widgets in a flexbox layout. """

    x, y = 0, 0
    positions: list[list[int]] = []
    max_height = max(heights)

    # Handle main alignment
    for i, width in enumerate(widths):
        # If wrapping is needed and current x exceeds the flex box width
        if flex_box_size[0] != 'auto' and wrap and x + width > flex_box_size[0]:
            x = 0
            y += (max_height + vertical_gap) if side_alignment != 'end' else -(max_height + vertical_gap)

        positions.append([x + gap, y])
        x += width + gap

    max_widget_height = max_height + vertical_gap
    flex_box_height = flex_box_size[1] if flex_box_size[1] != 'auto' else max_widget_height

    # Handle side alignment
    if side_alignment == 'center':
        center_y = flex_box_height // 2
        positions = [[pos[0] + gap, pos[1] + center_y - (max_widget_height // 2)] for pos in positions]
    elif side_alignment == 'end':
        positions = [[pos[0] + gap, pos[1] + (flex_box_height - max_widget_height)] for pos in positions]

    return positions


@lru_cache(maxsize=1000)
def HorizontalBox(widths: tuple[int, ...], heights: tuple[int, ...],
                 box_width: int | str = 'auto', box_height: int | str = 'auto',
                 alignment: str = 'start', side_alignment: str = 'start',
                 wrap: bool = False, gap: int = 5, vertical_gap: int = 5):

    if alignment == 'start':
        return calculate_start_positions(widths, heights, side_alignment, (box_width, box_height), wrap, gap, vertical_gap)


w = (100, 5, 100) * 100000
h = (30, 5, 30) * 100000


def benchmark():
    HorizontalBox(w, h)


if __name__ == '__main__':
    import cProfile
    cProfile.run('benchmark()')
