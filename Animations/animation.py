from .list_generator import generate_lists
from .initials_generator import generate_initials
from .easing_function_generator import generate_easing_function


class Animation:
    def __init__(self,
                 widget, name, end_value,
                 time: float = 0.3, curve='ease in out',
                 mode: str = "",
                 animation_finished=lambda: ...):
        # Initials
        self.widget = widget
        self.time = time
        self.name = name
        self.animation_finished = animation_finished
        self.mode = mode
        self.elapsed_time = 0

        self.window = widget.get_top_parent()

        self.start_value, self.end_value, self._type = generate_initials(name, end_value, widget)

        self._current_value = self.start_value

        self.easing_function = generate_easing_function(curve)
        self.listings = generate_lists(name, self._type, self.start_value, self.end_value, mode)

        if self.name == 'x':
            self.setter = lambda v: self.widget.set_position(self._current_value, self.widget.y)
        elif self.name == 'y':
            self.setter = lambda v: self.widget.set_position(self.widget.x, self._current_value)
        else:
            self.setter = lambda v: self.widget.set(self.name, self._current_value)

        self._after_function = None
        self._stop_elapsed_time = 0
        self._is_stopping = False
        self._stop_duration = 1

    def start(self):
        if self.start_value != self.end_value:
            self.window.add_update_function(self.update, parse_delta=True)
        else:
            self.animation_finished()

    def update(self, delta):
        if self._is_stopping:
            self._stop_elapsed_time += delta
            proportion = self.easing_function(min(self._stop_elapsed_time / self._stop_duration, 1))
            self.time += proportion * delta

            if self._stop_elapsed_time >= self._stop_duration:
                self._is_stopping = False
                self.window.remove_update_function(self.update)
                self.animation_finished()
                self._after_function()
                return

        self.elapsed_time += delta
        proportion = self.easing_function(min(self.elapsed_time / self.time, 1))

        index = int(proportion * (len(self.listings) - 1))
        index = max(min(index, len(self.listings) - 1), 0)

        self._current_value = self.listings[index]

        self.setter(self._current_value)

        if self._current_value == self.listings[-1]:
            self.window.remove_update_function(self.update)

            if self.name in ['x', 'y']:
                self.widget.set_position(self.end_value, self.widget.y) if self.name == 'x' else self.widget.set_position(self.widget.x, self._current_value)
            else:
                self.widget.set(self.name, self.end_value if not isinstance(self.end_value, str) else self.end_value.removesuffix('px'))

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

        self.window.after(int((break_speed * 1000)) - 100, lambda: Animation(widget=self.widget, name=self.name, end_value=new_end_value, time=other_speed, curve=self.easing_function, animation_finished=self.animation_finished).start())

