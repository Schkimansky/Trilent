# This is mainly using by the Text widget.
from PyQt6.QtCore import Qt
from typing import Literal

QT_DICT = {
    'top left':      Qt.AlignmentFlag.AlignTop     | Qt.AlignmentFlag.AlignLeft,
    'top center':    Qt.AlignmentFlag.AlignTop     | Qt.AlignmentFlag.AlignHCenter,
    'top right':     Qt.AlignmentFlag.AlignTop     | Qt.AlignmentFlag.AlignRight,
    'center left':   Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
    'center center': Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
    'center right':  Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
    'bottom left':   Qt.AlignmentFlag.AlignBottom  | Qt.AlignmentFlag.AlignLeft,
    'bottom center': Qt.AlignmentFlag.AlignBottom  | Qt.AlignmentFlag.AlignHCenter,
    'bottom right':  Qt.AlignmentFlag.AlignBottom  | Qt.AlignmentFlag.AlignRight,

    'center': Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
    'top'   : Qt.AlignmentFlag.AlignTop     | Qt.AlignmentFlag.AlignHCenter,
    'bottom': Qt.AlignmentFlag.AlignBottom  | Qt.AlignmentFlag.AlignHCenter,
    'left'  : Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
    'right' : Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
}


QT_DICT_LITERAL = Literal[
    'top left',
    'top center',
    'top right',
    'center left',
    'center center',
    'center right',
    'bottom left',
    'bottom center',
    'bottom right',
    'center',
    'top',
    'bottom',
    'left',
    'right']


def qt_orientation(name: QT_DICT_LITERAL):
    return QT_DICT[name]

