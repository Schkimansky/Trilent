from .fallback import fallback, CACHING_LIMIT, FUNCTIONS
from functools import lru_cache


@lru_cache(CACHING_LIMIT // FUNCTIONS)
def calculate_end_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int, side_alignment: str) -> list[list[int]]:
    if side_alignment == 'end':
        x, y = 0, flex_box_size[1]
    else:
        x, y = 0, 0

    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = 1
    total_height = 0
    total_width = 0
    total_width_calculated = False

    for i, width in enumerate(widths):
        if wrap and x + width > flex_box_size[0] and i != 0:
            x = 0
            if side_alignment == 'end':
                y -= max(column_heights) + vertical_gap
            else:
                y += max(column_heights) + vertical_gap
            total_height += max(column_heights) + vertical_gap

            wraps += 1
            column_heights = []
            total_width_calculated = True

        if side_alignment == 'end':
            positions.append([x, y - heights[i]])
        else:
            positions.append([x, y])

        column_heights.append(heights[i])
        x += width + gap
        if not total_width_calculated:
            total_width += width + gap

    total_height += max(column_heights) + vertical_gap if column_heights else 0

    # Fallback is used to fix a bug, You can ignore this.
    if wraps >= len(widths):
        positions, first_col_h, _ = fallback(positions, heights, vertical_gap, side_alignment, flex_box_size[1])

    # Center Y Positions if requested.
    if side_alignment == 'center':
        adder = (flex_box_size[1] // 2) - (total_height // 2)
        positions = [[pos[0], pos[1] + adder] for pos in positions]

    # End point all x positions
    for pos in positions:
        pos[0] += flex_box_size[0] - total_width

    return positions
