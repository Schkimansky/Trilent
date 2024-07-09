from .general import fallback, CACHING_LIMIT, FUNCTIONS, center_y_positions
from functools import lru_cache


@lru_cache(CACHING_LIMIT // FUNCTIONS)
def calculate_center_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int, side_alignment: str) -> list[list[int]]:
    if side_alignment == 'end':
        x, y = 0, flex_box_size[1]
    else:
        x, y = 0, 0

    positions: list[list[int]] = []
    column_heights: list[int] = []
    row_start_index = 0
    wraps = 1
    total_height = 0

    for i, width in enumerate(widths):
        if wrap and x + width > flex_box_size[0] and i != 0:
            # Center the previous row
            row_width = x - gap
            shift = (flex_box_size[0] - row_width) // 2
            for j in range(row_start_index, i):
                positions[j][0] += shift

            # Start new row
            row_start_index = i
            x = 0
            if side_alignment == 'end':
                y -= max(column_heights) + vertical_gap
            else:
                y += max(column_heights) + vertical_gap
            total_height += max(column_heights) + vertical_gap

            wraps += 1
            column_heights = []

        if side_alignment == 'end':
            positions.append([x, y - heights[i]])
        else:
            positions.append([x, y])

        column_heights.append(heights[i])
        x += width + gap

    # Center the last row
    if row_start_index < len(widths):
        row_width = x - gap
        shift = (flex_box_size[0] - row_width) // 2
        for j in range(row_start_index, len(widths)):
            positions[j][0] += shift

    total_height += max(column_heights) if column_heights else 0

    # Fallback is used to fix a bug, You can ignore this.
    if wraps >= len(widths):
        positions = fallback(positions, heights, vertical_gap, side_alignment, flex_box_size[1])

    if side_alignment == 'center':
        positions = center_y_positions(positions, flex_box_size, total_height)

    return positions
