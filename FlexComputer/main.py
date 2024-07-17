from .start_alignment import calculate_start_positions
from .center_alignment import calculate_center_positions
from .end_alignment import calculate_end_positions


def box(widths: tuple[int, ...], heights: tuple[int, ...], box_width: int = 500, box_height: int = 500, alignment: str = 'start', side_alignment: str = 'start', wrap: bool = False, gap: int = 5, vertical_gap: int = 5):
    arguments = (widths, heights, (box_width, box_height), wrap, gap, vertical_gap, side_alignment)

    # Different functions for different scenarios because of speed.
    if alignment == 'start':
        return calculate_start_positions(*arguments)
    elif alignment == 'center':
        return calculate_center_positions(*arguments)
    elif alignment == 'end':
        return calculate_end_positions(*arguments)
