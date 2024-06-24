# This is mainly using by the Text widget.
from PyQt5.Qt import Qt
from typing import Literal

QT_DICT = {
    'top left': Qt.AlignTop | Qt.AlignLeft,
    'top center': Qt.AlignTop | Qt.AlignHCenter,
    'top right': Qt.AlignTop | Qt.AlignRight,
    'middle left': Qt.AlignVCenter | Qt.AlignLeft,
    'middle center': Qt.AlignVCenter | Qt.AlignHCenter,
    'middle right': Qt.AlignVCenter | Qt.AlignRight,
    'bottom left': Qt.AlignBottom | Qt.AlignLeft,
    'bottom center': Qt.AlignBottom | Qt.AlignHCenter,
    'bottom right': Qt.AlignBottom | Qt.AlignRight,

    'center': Qt.AlignVCenter | Qt.AlignHCenter,
    'top': Qt.AlignTop | Qt.AlignHCenter,
    'bottom': Qt.AlignBottom | Qt.AlignHCenter,
    'left': Qt.AlignVCenter | Qt.AlignLeft,
    'right': Qt.AlignVCenter | Qt.AlignRight
}


QT_DICT_LITERAL = Literal[
    'top left',
    'top center',
    'top right',
    'middle left',
    'middle center',
    'middle right',
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

