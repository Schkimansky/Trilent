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
    column_widths: list[list[int]] = [[]]
    column_widths_map: dict[int, int] = {}
    wraps: int = 1
    total_height: int = 0
    total_width: int = 0
    total_width_calculated: bool = False

    for i in range(len(widths)):
        if wrap and x + widths[i] > flex_box_size[0] and i != 0:
            x = 0
            if side_alignment == 'end':
                y -= max(column_heights) + vertical_gap
            else:
                y += max(column_heights) + vertical_gap
            total_height += max(column_heights) + vertical_gap

            wraps += 1
            column_heights = []
            column_widths.append([])
            total_width_calculated = True

        if side_alignment == 'end':
            positions.append([x, y - heights[i]])
        else:
            positions.append([x, y])

        column_heights.append(heights[i])
        column_widths[wraps - 1].append(widths[i] + gap)
        column_widths_map[i] = wraps - 1

        x += widths[i] + gap
        if not total_width_calculated:
            total_width += widths[i] + gap

    total_height += max(column_heights) + vertical_gap if column_heights else 0

    # Fallback is used to fix a bug, You can ignore this.
    if wraps >= len(widths):
        positions, first_col_h, _ = fallback(positions, heights, vertical_gap, side_alignment, flex_box_size[1])

    # Center Y Positions if requested.
    if side_alignment == 'center':
        adder = (flex_box_size[1] // 2) - (total_height // 2)
        positions = [[pos[0], pos[1] + adder] for pos in positions]

    # End point all x positions
    for i, pos in enumerate(positions):
        # How do i figure out current column widths
        pos[0] += flex_box_size[0] - sum(column_widths[column_widths_map[i]])
        print(column_widths)

    return positions
