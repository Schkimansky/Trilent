CACHING_LIMIT = 1000
FUNCTIONS = 3


def fallback(positions, heights, vertical_gap, side_alignment='start', flex_box_height=0) -> tuple[list[list[int]], int, int]:
    if side_alignment in ['start', 'center']:
        y = 0
        flex_box_height = 0
        highest_first_column_widget_height = heights[0]
        for i, pos in enumerate(positions):
            positions[i] = [pos[0], y]
            y += heights[i] + vertical_gap
            flex_box_height += heights[i] + vertical_gap

        return positions, flex_box_height, highest_first_column_widget_height
    else:
        y = flex_box_height - vertical_gap
        highest_first_column_widget_height = heights[0]

        for i, pos in enumerate(positions):
            positions[i] = [pos[0], y]
            y -= vertical_gap + heights[i]
            flex_box_height += vertical_gap + heights[i]

        return positions, flex_box_height, highest_first_column_widget_height

