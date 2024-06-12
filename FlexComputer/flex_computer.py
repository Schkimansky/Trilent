
def calculate_start_positions(lengths: list[int], flex_box_size: tuple[int | str, int | str]) -> list[list[int]]:
    extra_space: list[int] = [0, 0]
    minimum_box_space: list[int] = [0, 0]
    positions: list[list[int]] = []
    box_size: list[int] = [0, 0]

    for length in lengths:
        positions.append(extra_space)
        # Make x ( / y / side / main) room for next widget
        extra_space[0] += length

    return positions


class Computer:
    def __init__(self, widths: list[int], heights: list[int],
                 flexing_direction: str = 'horizontal',
                 box_width: int | str = 'auto', box_height: int | str = 'auto',
                 alignment: str = 'start', side_alignment: str = 'start'):

        main_axis_lengths = widths if flexing_direction == 'horizontal' else heights
        side_axis_lengths = heights if flexing_direction == 'horizontal' else widths
        flex_box_size = (box_width, box_height)

        match alignment:
            case "start":
                main_axis = calculate_start_positions(main_axis_lengths, flex_box_size)
            case _:
                raise ValueError(f'Invalid alignment name: {alignment}')

        match side_alignment:
            case "start":
                side_axis = calculate_start_positions(side_axis_lengths, flex_box_size)
            case _:
                raise ValueError(f'Invalid side alignment name: {side_alignment}')

        print(main_axis)
        print("next")
        print(side_axis)


if __name__ == '__main__':
    width = [100, 100, 100]
    height = [100, 100, 100]
    Computer(width, height)
