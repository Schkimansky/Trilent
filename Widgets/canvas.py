from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QPen, QColor, QBrush, QPainter
from PyQt6.QtCore import Qt, QRect
from trilent.Utility import Reloader, V, Misc
from trilent.Widgets import PositionTypes


class Shape:
    def __init__(self, qt_item: QGraphicsRectItem):
        self._qt_item = qt_item

    @property
    def x(self): return self._qt_item.x()
    @property
    def y(self): return self._qt_item.y()
    @property
    def width(self): return self._qt_item.rect().width()
    @property
    def height(self): return self._qt_item.rect().height()
    @property
    def scale(self): return self._qt_item.scale()
    @property
    def opacity(self): return self._qt_item.opacity()

    def set_scale(self, scale): return self._qt_item.setScale(scale)
    def set_opacity(self, opacity): return self._qt_item.setOpacity(opacity)

    def set_position(self, x, y):
        self._qt_item.setX(x)
        self._qt_item.setY(y)

    def set_size(self, width, height):
        self._qt_item.setRect(QRect(self.x, self.y, width, height))
        self._qt_item.scale()


class Canvas(Misc):
    def __init__(self,
                 parent,
                 # Special
                 width      : int | str = None,
                 height     : int | str = None,

                 # Stylesheet
                 background_color: str = None,
                 border_color    : str = None,
                 border_width    : str | int = None):

        # Reloader setup
        base = f"""QGraphicsView {{ background-color: {V}background_color{V}; border: {V}border_width{V} solid {V}border_color{V}; }}"""

        self._reloader = Reloader(parent.get_dpi(),
                                  setup_properties  = {'background_color': background_color,   'border_color': border_color,       'border_width': border_width,  'parent': parent,   'width': width,          'height': height},
                                  process_types     = {'background_color': 'color',            'border_color': 'color',            'border_width': 'px-value',    'parent': None,     'width': 'px-value;int', 'height': 'px-value;int'},
                                  default_values    = {'background_color': '#272727',          'border_color': '255, 255, 255, 3', 'border_width': 0,             'parent': None,     'width': '5 inch',       'height': '5 inch'},
                                  property_types    = {'background_color': 'stylesheet',       'border_color': 'stylesheet',       'border_width': 'stylesheet',  'parent': 'access', 'width': 'special',      'height': 'special'},
                                  special_functions = {'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
                                  base              = base)

        # Protected widget specific members
        self._position_self = self._reloader.cp['parent']._position_children
        self._position_children = PositionTypes.NONE
        self._dpi = parent.get_dpi()

        # Qt setup
        self._scene = QGraphicsScene()
        self._widget = QGraphicsView(self._scene, self._reloader.cp['parent']._get_holder())

        # Setup properties
        self._widget.setFixedSize(width, height)
        self._scene.setSceneRect(0,0, width, height)
        self._widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._widget.setStyleSheet(self._reloader.reload())

        # Check if Canvas's parent is also a box
        if self._reloader.cp['parent']._position_children == PositionTypes.BOX:
            self._reloader.cp['parent']._widget_box_add(self)

    def square(self, x, y, width, height, color='white', border_color='black', border_width=1):
        rect = self._scene.addRect(x, y, width, height, QPen(QColor(border_color), border_width), QBrush(QColor(color)))
        return rect

    def circle(self, x, y, width, height, color='white', border_color='black', border_width=1):
        circle = self._scene.addEllipse(x, y, width, height, QPen(QColor(border_color), border_width), QBrush(QColor(color)))
        return Shape(circle)

    def line(self, x1, y1, x2, y2, color='white', width=1):
        line = self._scene.addLine(x1, y1, x2, y2, QPen(QColor(color), width))
        return Shape(line)

    def text(self, x, y, text, color='white', font=None):
        text_item = self._scene.addText(text)
        text_item.setDefaultTextColor(QColor(color))
        text_item.setPos(x, y)
        if font:
            text_item.setFont(font)
        return Shape(text_item)

    def clear(self):
        self._scene.clear()

    def set_size(self, width, height):
        self._widget.setFixedSize(width, height)
        self._scene.setSceneRect(0, 0, width, height)

    def set_pixel(self, x, y, color):
        self._scene.addRect(x, y, 1, 1, QPen(Qt.PenStyle.NoPen), QBrush(QColor(color)))
