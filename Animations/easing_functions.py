import math


class EasingFunctions:
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
    def back_out(t, s=1.70158):
        t -= 1
        return t * t * ((s + 1) * t + s) + 1

    @staticmethod
    def back_in(t, s=1.70158):
        return t * t * ((s + 1) * t - s)

    @staticmethod
    def back_in_out(t, s=1.70158):
        t *= 2
        if t < 1:
            return 0.5 * (t * t * ((s + 1) * t - s))
        t -= 2
        return 0.5 * (t * t * ((s + 1) * t + s) + 2)

    @staticmethod
    def sine_in(t):
        return 1 - math.cos((t * math.pi) / 2)

    @staticmethod
    def sine_out(t):
        return math.sin((t * math.pi) / 2)

    @staticmethod
    def sine_in_out(t):
        return -(math.cos(math.pi * t) - 1) / 2

    @staticmethod
    def quad_in(t):
        return t * t

    @staticmethod
    def quad_out(t):
        return t * (2 - t)

    @staticmethod
    def quad_in_out(t):
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def cubic_in(t):
        return t * t * t

    @staticmethod
    def cubic_out(t):
        return (--t) * t * t + 1

    @staticmethod
    def cubic_in_out(t):
        return 4 * t * t * t if t < 0.5 else (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def quart_in(t):
        return t * t * t * t

    @staticmethod
    def quart_out(t):
        return 1 - (--t) * t * t * t

    @staticmethod
    def quart_in_out(t):
        return 8 * t * t * t * t if t < 0.5 else 1 - 8 * (--t) * t * t * t

    @staticmethod
    def quint_in(t):
        return t * t * t * t * t

    @staticmethod
    def quint_out(t):
        return 1 + (--t) * t * t * t * t

    @staticmethod
    def quint_in_out(t):
        return 16 * t * t * t * t * t if t < 0.5 else 1 + 16 * (--t) * t * t * t * t

    @staticmethod
    def expo_in(t):
        return 0 if t == 0 else math.pow(2, 10 * (t - 1))

    @staticmethod
    def expo_out(t):
        return 1 if t == 1 else 1 - math.pow(2, -10 * t)

    @staticmethod
    def expo_in_out(t):
        if t == 0:
            return 0
        if t == 1:
            return 1
        return math.pow(2, 10 * (2 * t - 1)) / 2 if t < 0.5 else (2 - math.pow(2, -10 * (2 * t - 1))) / 2

    @staticmethod
    def circle_in(t):
        return 1 - math.sqrt(1 - t * t)

    @staticmethod
    def circle_out(t):
        return math.sqrt(1 - (--t) * t)

    @staticmethod
    def circle_in_out(t):
        return (1 - math.sqrt(1 - 4 * t * t)) / 2 if t < 0.5 else (math.sqrt(1 - (2 * t - 2) * (2 * t - 2)) + 1) / 2

    @staticmethod
    def linear(t):
        return t

    @staticmethod
    def linear_in(t):
        return t

    @staticmethod
    def linear_out(t):
        return t

    @staticmethod
    def linear_in_out(t):
        return t
