from .easing_functions import EasingFunctions


def generate_easing_function(curve: str):
    return getattr(EasingFunctions, curve.replace(' ', '_'))
