from functools import lru_cache


def fallback(positions, heights, vertical_gap) -> tuple[list[list[int]], int, int]:
    y = 0
    flex_box_height = 0
    highest_first_column_widget_height = heights[0]
    for i, pos in enumerate(positions):
        positions[i] = [pos[0], y]
        y += heights[i] + vertical_gap
        flex_box_height += heights[i] + vertical_gap

    return positions, flex_box_height, highest_first_column_widget_height


#
#   Calculation Functions
#

# The reason there is a different function for each side alignment and alignment scenario is because of speed.


CACHING_LIMIT = 1000
FUNCTIONS = 3


#
# Start Alignment
#


@lru_cache(maxsize=CACHING_LIMIT // FUNCTIONS)
def calculate_start_start_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int) -> list[list[int]]:
    x, y = 0, 0
    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = -(-sum(widths) // flex_box_size[0])

    # Handle main alignment
    for i, width in enumerate(widths):
        # If wrapping is needed and current x exceeds the flex box width (To fix a bug i put: unless the index is 0)
        if wrap and x + width > flex_box_size[0] and i != 0:
            x = 0
            y += max(column_heights) + vertical_gap if column_heights else 0

            column_heights = []

        positions.append([x, y])
        column_heights.append(heights[i])
        x += width + gap

    # Fix: When Flex_box_width is so low that all the widgets wrap on top,
    # It adds y to max_height instead of last widgets height
    if wraps >= len(widths):
        positions, flex_box_height, highest_first_column_widget_height = fallback(positions, heights, vertical_gap)

    return positions


@lru_cache(maxsize=CACHING_LIMIT // FUNCTIONS)
def calculate_start_center_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int) -> list[list[int]]:
    x, y = 0, 0
    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = 1
    total_height = 0

    for i, width in enumerate(widths):
        # If wrapping is needed and current x exceeds the flex box width.
        if wrap and x + width > flex_box_size[0] and i != 0:
            x = 0
            y += max(column_heights) + vertical_gap if column_heights else 0
            total_height += max(column_heights) + vertical_gap if column_heights else 0
            wraps += 1

            column_heights = []

        positions.append([x, y])
        column_heights.append(heights[i])
        x += width + gap

    total_height += max(column_heights) + vertical_gap if column_heights else 0

    # Fix: When Flex_box_width is so low that all the widgets wrap on top,
    # It adds y to max_height instead of last widgets height
    if wraps >= len(widths):
        positions, _, _ = fallback(positions, heights, vertical_gap)

    adder = (flex_box_size[1] // 2) - (total_height // 2)
    positions = [[pos[0], pos[1] + adder] for pos in positions]

    return positions


@lru_cache(maxsize=CACHING_LIMIT // FUNCTIONS)
def calculate_start_end_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int) -> list[list[int]]:
    x, y = 0, flex_box_size[1]  # Start y from the height of the container
    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = 1

    for i, width in enumerate(widths):
        if wrap and x + width > flex_box_size[0] and i != 0:
            x = 0
            y -= max(column_heights) + vertical_gap  # Move y downwards for wrapping
            wraps += 1

            column_heights = []

        positions.append([x, y - heights[i]])
        column_heights.append(heights[i])
        x += width + gap

    if wraps >= len(widths):
        positions, first_col_h, _ = fallback(positions, heights, vertical_gap)

    return positions


#
# Center Alignment
#


@lru_cache(maxsize=CACHING_LIMIT // FUNCTIONS)
def calculate_center_start_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int) -> list[list[int]]:
    x, y = 0, 0
    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = -(-sum(widths) // flex_box_size[0])

    # Handle main alignment
    for i, width in enumerate(widths):
        # If wrapping is needed and current x exceeds the flex box width (To fix a bug i put: unless the index is 0)
        if wrap and x + width > flex_box_size[0] and i != 0:
            x = 0
            y += heights[i] + vertical_gap if column_heights else 0

            column_heights = []

        positions.append([x, y])
        column_heights.append(heights[i])
        x += width + gap

    # Fix: When Flex_box_width is so low that all the widgets wrap on top,
    # It adds y to max_height instead of last widgets height
    if wraps >= len(widths):
        positions, flex_box_height, highest_first_column_widget_height = fallback(positions, heights, vertical_gap)

    return positions

#
# Importing
#


def HorizontalBox(widths: tuple[int, ...], heights: tuple[int, ...], box_width: int = 500, box_height: int = 500, alignment: str = 'start', side_alignment: str = 'start', wrap: bool = False, gap: int = 5, vertical_gap: int = 5):

    arguments = (widths, heights, (box_width, box_height), wrap, gap, vertical_gap)

    # Different functions for different scenarios because of speed.
    if alignment == 'start' and side_alignment == 'start':
        return calculate_start_start_positions(*arguments)
    elif alignment == 'start' and side_alignment == 'center':
        return calculate_start_center_positions(*arguments)
    elif alignment == 'start' and side_alignment == 'end':
        return calculate_start_end_positions(*arguments)

    elif alignment == 'center' and side_alignment == 'start':
        return calculate_center_start_positions(*arguments)


if __name__ == '__main__':
    print('Dont mess with the libraries code, You\'ll probably mess it up.')
