CACHING_LIMIT = 10
FUNCTIONS = 9


def fallback(positions, heights, vertical_gap, side_alignment='start', flex_box_height=0) -> list[list[int]]:
    y = 0 if side_alignment in ['start', 'center'] else flex_box_height - heights[0]

    for i, pos in enumerate(positions):
        positions[i] = [pos[0], y]

        if side_alignment != 'end':
            y += heights[i] + vertical_gap
        else:
            y -= vertical_gap + heights[i]

    return positions


def center_y_positions(positions: list[list[int]], flex_box_size: tuple[int, int], total_height: int) -> list[list[int]]:
    adder = (flex_box_size[1] // 2) - (total_height // 2)
    return [[pos[0], pos[1] + adder] for pos in positions]

