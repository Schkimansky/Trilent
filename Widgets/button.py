from PyQt5.QtWidgets import QPushButton
from Trilent.Window import Window


class Button:
    def __init__(self, parent: Window):
        self._widget = QPushButton(parent._get_holder())
