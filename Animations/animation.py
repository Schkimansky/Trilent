import math
from trilent.Utility.gradient_list import color_gradient, gradient_gradient, convert_rgba_to_hex, convert_hex_to_rgba


def better_range(start_value, end_value):
    if start_value < end_value:
        ranges = list(range(start_value, end_value + 1))
    else:
        ranges = list(range(start_value, end_value, -1))
    return ranges


class Animation:
    def __init__(self, widget, name, end_value, time: float = 0.3, curve='ease in out', animation_finished=lambda: ...):
        # Initials
        self._after_function = None
        self.widget = widget
        self.time = time
        self.name = name
        self.animation_finished = animation_finished

        # Top level window
        self._window = widget.get_top_parent()

        # Defining Values
        if name in ['x', 'y']:
            self._start_value = getattr(widget, name)
            self._end_value = widget._reloader.alternate_process('px-value;int', end_value)
            self._type = 'px-value;int'
            self._raw_start_value = getattr(widget, name)
            self._raw_end_value = end_value
        elif end_value.__contains__(' -> '):
            self._start_value = widget.get(name)
            if not self._start_value.__contains__(' -> '):
                self._start_value = f"{self._start_value} -> {self._start_value}"

            self._end_value = end_value
            self._type = 'gradient color'
            self._raw_start_value = self._start_value
            self._raw_end_value = end_value
        else:
            self._start_value = self.widget._reloader.process(self.name, widget._reloader.cp[name])
            self._end_value = widget._reloader.process(name, end_value)
            self._type = widget._reloader.initial_parameters['process_types'][name]
            self._raw_start_value = widget._reloader.cp[name]
            self._raw_end_value = end_value

        self._current_value = self._start_value

        # Animation variables
        self.elapsed_time = 0

        if isinstance(curve, str):
            self._easing_function = getattr(self, curve.replace(' ', '_'))
        elif curve is None:
            self._easing_function = self.ease_in_out_sine
        else:
            self._easing_function = curve

        self.listings = self._generate_listings()

        # Breaker variables
        self._is_stopping = False
        self._stop_elapsed_time = 0
        self._stop_duration = 1

    def start(self):
        if self._start_value != self._end_value:
            self._window.add_update_function(self.update, parse_delta=True)
        else:
            self.animation_finished()

    def update(self, delta):
        if self._is_stopping:
            self._stop_elapsed_time += delta
            proportion = self._easing_function(min(self._stop_elapsed_time / self._stop_duration, 1))
            self.time += proportion * delta

            if self._stop_elapsed_time >= self._stop_duration:
                self._is_stopping = False
                self._window.remove_update_function(self.update)
                self.animation_finished()
                self._after_function()
                return

        self.elapsed_time += delta
        proportion = self._easing_function(min(self.elapsed_time / self.time, 1))

        index = int(proportion * (len(self.listings) - 1))
        index = max(min(index, len(self.listings) - 1), 0)

        self._current_value = self.listings[index]

        if self.name in ['x', 'y']:
            self.widget.set_position(self._current_value, self.widget.y) if self.name == 'x' else self.widget.set_position(self.widget.x, self._current_value)
        else:
            self.widget.set(self.name, self._current_value)

        if self._current_value == self.listings[-1]:
            self._window.remove_update_function(self.update)

            if self.name in ['x', 'y']:
                self.widget.set_position(self._end_value, self.widget.y) if self.name == 'x' else self.widget.set_position(self.widget.x, self._current_value)
            else:
                self.widget.set(self.name, self._end_value if not isinstance(self._end_value, str) else self._end_value.removesuffix('px'))

            self.animation_finished()

    def stop(self, stop_duration=1, after_function=lambda: ...):
        self._is_stopping = True
        self._stop_duration = stop_duration
        self._stop_elapsed_time = 0
        self._after_function = after_function

    def change(self, new_end_value=None, break_speed=None, other_speed=None):
        if new_end_value is None:
            new_end_value = self._current_value
        if break_speed is None:
            break_speed = 0.1
        if other_speed is None:
            other_speed = self.time - self.elapsed_time

        self.stop(break_speed)

        break_speed = max(break_speed, 0.1)

        self._window.after(int((break_speed * 1000)) - 100, lambda: Animation(widget=self.widget, name=self.name, end_value=new_end_value, time=other_speed, curve=self._easing_function, animation_finished=self.animation_finished).start())

    def _generate_listings(self):
        match self._type:
            case 'px-value;int':
                listings = better_range(self._start_value, self._end_value)
            case 'px-value':
                listings = better_range(self.break_px(self._start_value), self.break_px(self._end_value))
            case 'gradient color':
                listings = gradient_gradient(self._start_value, self._end_value, 255, 30,
                                             self.widget._reloader.alternate_process)
            case 'color':
                listings = color_gradient(self._start_value, self._end_value, 255)
            case _:
                raise NotImplementedError(f'Animations for "{self.name}" isn\'t supported yet. Type: {self._type}')
        return listings

    @staticmethod
    def break_px(string: str):
        return int(string.removesuffix('px'))

    @staticmethod
    def ease_in(t):
        return t * t * t

    @staticmethod
    def ease_out(t):
        t -= 1
        return t * t * t + 1

    @staticmethod
    def ease_in_out(t):
        t *= 2
        if t < 1:
            return 0.5 * t * t * t
        t -= 2
        return 0.5 * (t * t * t + 2)

    @staticmethod
    def ease_out_back(t, s=1.70158):
        t -= 1
        return t * t * ((s + 1) * t + s) + 1

    @staticmethod
    def ease_in_back(t, s=1.70158):
        return t * t * ((s + 1) * t - s)

    @staticmethod
    def ease_in_out_back(t, s=1.70158):
        t *= 2
        if t < 1:
            return 0.5 * (t * t * ((s + 1) * t - s))
        t -= 2
        return 0.5 * (t * t * ((s + 1) * t + s) + 2)

    @staticmethod
    def ease_in_sine(t):
        return 1 - math.cos((t * math.pi) / 2)

    @staticmethod
    def ease_out_sine(t):
        return math.sin((t * math.pi) / 2)

    @staticmethod
    def ease_in_out_sine(t):
        return -(math.cos(math.pi * t) - 1) / 2

    @staticmethod
    def ease_in_quad(t):
        return t * t

    @staticmethod
    def ease_out_quad(t):
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t):
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t):
        return t * t * t

    @staticmethod
    def ease_out_cubic(t):
        return (--t) * t * t + 1

    @staticmethod
    def ease_in_out_cubic(t):
        return 4 * t * t * t if t < 0.5 else (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def ease_in_quart(t):
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t):
        return 1 - (--t) * t * t * t

    @staticmethod
    def ease_in_out_quart(t):
        return 8 * t * t * t * t if t < 0.5 else 1 - 8 * (--t) * t * t * t

    @staticmethod
    def ease_in_quint(t):
        return t * t * t * t * t

    @staticmethod
    def ease_out_quint(t):
        return 1 + (--t) * t * t * t * t

    @staticmethod
    def ease_in_out_quint(t):
        return 16 * t * t * t * t * t if t < 0.5 else 1 + 16 * (--t) * t * t * t * t

    @staticmethod
    def ease_in_expo(t):
        return 0 if t == 0 else math.pow(2, 10 * (t - 1))

    @staticmethod
    def ease_out_expo(t):
        return 1 if t == 1 else 1 - math.pow(2, -10 * t)

    @staticmethod
    def ease_in_out_expo(t):
        if t == 0:
            return 0
        if t == 1:
            return 1
        return math.pow(2, 10 * (2 * t - 1)) / 2 if t < 0.5 else (2 - math.pow(2, -10 * (2 * t - 1))) / 2

    @staticmethod
    def ease_in_circle(t):
        return 1 - math.sqrt(1 - t * t)

    @staticmethod
    def ease_out_circle(t):
        return math.sqrt(1 - (--t) * t)

    @staticmethod
    def ease_in_out_circle(t):
        return (1 - math.sqrt(1 - 4 * t * t)) / 2 if t < 0.5 else (math.sqrt(1 - (2 * t - 2) * (2 * t - 2)) + 1) / 2

    @staticmethod
    def linear(t):
        return t
