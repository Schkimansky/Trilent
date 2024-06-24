from .general import fallback, CACHING_LIMIT, FUNCTIONS, center_y_positions
from functools import lru_cache


@lru_cache(CACHING_LIMIT // FUNCTIONS)
def calculate_start_positions(widths: tuple[int, ...], heights: tuple[int, ...], flex_box_size: tuple[int | str, int | str], wrap: bool, gap: int, vertical_gap: int, side_alignment: str) -> list[list[int]]:
    if side_alignment == 'end':
        # Start y from the height of the container
        x, y = 0, flex_box_size[1]
    else:
        x, y = 0, 0

    positions: list[list[int]] = []
    column_heights: list[int] = []
    wraps = 1
    # Side alignment center
    total_height = 0

    for i, width in enumerate(widths):
        if wrap and x + width > flex_box_size[0] and i != 0:
            x = 0
            if side_alignment == 'end':
                y -= max(column_heights) + vertical_gap  # Move y downwards for wrapping
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

    total_height += max(column_heights) + vertical_gap if column_heights else 0

    if wraps >= len(widths): positions = fallback(positions, heights, vertical_gap, side_alignment, flex_box_size[1])
    if side_alignment == 'center': positions = center_y_positions(positions, flex_box_size, total_height)

    return positions

