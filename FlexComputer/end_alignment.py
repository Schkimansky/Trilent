from .general import fallback, CACHING_LIMIT, FUNCTIONS, center_y_positions
from functools import lru_cache


@lru_cache(CACHING_LIMIT // FUNCTIONS)
def calculate_end_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int, side_alignment: str) -> list[list[int]]:
    if side_alignment == 'end':
        x, y = 0, flex_box_size[1]
    else:
        x, y = 0, 0

    positions: list[list[int]] = []
    column_heights: list[int] = []
    column_widths: list[list[int]] = [[]]
    column_widths_map: dict[int, int] = {}
    wraps: int = 1
    total_height: int = 0

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
            column_widths.append([])

        if side_alignment == 'end':
            positions.append([x, y - heights[i]])
        else:
            positions.append([x, y])

        column_heights.append(heights[i])
        column_widths[wraps - 1].append(widths[i] + gap)
        column_widths_map[i] = wraps - 1

        x += widths[i] + gap

    total_height += max(column_heights) + vertical_gap if column_heights else 0

    # Fallback is used to fix a bug, You can ignore this.
    if wraps >= len(widths):
        positions = fallback(positions, heights, vertical_gap, side_alignment, flex_box_size[1])
        positions = [[pos[0], pos[1] - heights[-1]] for pos in positions]

    if side_alignment == 'center':
        positions = center_y_positions(positions, flex_box_size, total_height)

    # End point all x positions and return them
    return [[pos[0] + flex_box_size[0] - sum(column_widths[column_widths_map[i]]) + gap, pos[1]] for i, pos in enumerate(positions)]
