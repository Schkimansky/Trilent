from trilent.Widgets import Widget


class Spacer(Widget):
    def __init__(self,
                 parent,
                 # Special
                 width      : int | str = None,
                 height     : int | str = None):
        super().__init__(parent, width, height, widget_color='transparent')
