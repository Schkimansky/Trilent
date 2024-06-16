from functools import lru_cache


def fallback(positions, heights, vertical_gap) -> list[list[int]]:
    y = 0
    for i, pos in enumerate(positions):
        positions[i] = [pos[0], y]
        y += heights[i] + vertical_gap

    return positions


@lru_cache(maxsize=100)
def calculate_start_positions(widths: tuple[int, ...], heights: tuple[int, ...],
                              side_alignment: str,
                              flex_box_size: tuple[int | str, int | str],
                              wrap: bool, gap: int, vertical_gap: int) -> list[list[int]]:
    """ This function calculates the starting positions for widgets in a flexbox layout. """

    x, y = 0, 0
    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = -(-sum(widths) // flex_box_size[0])

    if side_alignment != 'end':
        # Handle main alignment
        for i, width in enumerate(widths):
            # If wrapping is needed and current x exceeds the flex box width (To fix a bug i put: unless the index is 0)
            if flex_box_size[0] != 'auto' and wrap and x + width > flex_box_size[0] and i != 0:
                x = 0
                # Instead of max(heights of all the widgets), get the max height of the widgets in the last column
                y += max(column_heights) + vertical_gap if column_heights else 0
                column_heights = []

            positions.append([x, y])
            column_heights.append(heights[i])
            x += width + gap
    elif side_alignment == 'end':
        # Handle main alignment
        for i, width in enumerate(widths):
            # If wrapping is needed and current x exceeds the flex box width (To fix a bug i put: unless the index is 0)
            if flex_box_size[0] != 'auto' and wrap and x + width > flex_box_size[0] and i != 0:
                x = 0
                # Instead of max(heights of all the widgets), get the max height of the widgets in the last column
                y -= max(column_heights) + vertical_gap if column_heights else 0
                column_heights = []

            positions.append([x, y])
            column_heights.append(heights[i])
            x += width + gap

    _, flex_box_height = flex_box_size

    # Handle side alignment

    # Fix: When Flex_box_width is so low that all the widgets wrap on top,
    # It adds y to max_height instead of last widgets height
    if wraps == len(widths):
        positions = fallback(positions, heights, vertical_gap)

    if side_alignment == 'center':
        average_height = sum(heights) // len(heights)
        positions = [[pos[0] + gap, pos[1] + (flex_box_height // 2) - (y // 2) - (average_height // 2) + (vertical_gap // 2)] for pos in positions]
    elif side_alignment == 'end':
        y += max(column_heights) + vertical_gap if column_heights else 0
        max_height = max(heights)

        print(flex_box_height, y)
        positions = [[pos[0] + gap, pos[1] + flex_box_height - max_height] for pos in positions]

    return positions


def HorizontalBox(widths: tuple[int, ...], heights: tuple[int, ...],
                 box_width: int = 500, box_height: int = 500,
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
