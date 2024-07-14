# from Trilent.Utility import Reloader, V, Misc
# from Trilent.Widgets import PositionTypes
# from Trilent.Widgets.button import Button
# from Trilent.Widgets.box import Box
# from typing import Literal
#
#
# class Option:
#     def __init__(self,
#                  # Special
#                  text       : str       = 'Trilent Option',
#                  text_size  : str | int = None,
#                  font       : str       = None,
#                  width      : int | str = None,
#                  height     : int | str = None,
#                  command    : lambda: ... = None,
#
#                  # Stylesheet
#                  text_color      : str = None,
#                  button_color    : str = '255, 255, 255, 10',
#                  corner_roundness: str | int = 0,
#                  hover_color     : str = '200, 200, 200, 20',
#                  clicked_color   : str = '150, 150, 150, 20',
#
#                  options: list = None,
#                  menu_corner_roundness: str | int = None,
#                  menu_open_side: Literal['bottom', 'right'] = 'right'):
#         if options is None:
#             options = []
#
#         self.args = (text,
#                      text_size,
#                      font,
#                      width,
#                      height,
#                      command,
#                      text_color,
#                      button_color,
#                      corner_roundness,
#                      hover_color,
#                      clicked_color,
#                      options,
#                      menu_corner_roundness,
#                      menu_open_side)
#
#
# class Menu(Misc):
#     def __init__(self,
#                  parent = None,
#                  # Special
#                  text       : str       = 'Menu',
#                  text_size  : str | int = None,
#                  font       : str       = None,
#                  width      : int | str = None,
#                  height     : int | str = None,
#                  command    : lambda: ... = None,
#
#                  # Stylesheet
#                  text_color      : str = None,
#                  button_color    : str = '255, 255, 255, 10',
#                  corner_roundness: str | int = 0,
#                  hover_color     : str = '200, 200, 200, 20',
#                  clicked_color   : str = '150, 150, 150, 20',
#
#                  options: list = None,
#                  menu_corner_roundness: str | int = None,
#                  menu_open_side: Literal['bottom', 'right'] = 'bottom'):
#
#         def trigger():
#             self._reloader2.cp['command']()
#             if self._state == 1:
#                 self.hide_menu()
#                 self._state = 0
#             else:
#                 self.show_menu()
#                 self._state = 1
#
#         self._widget = Button(parent, text, text_size, font, width, height, trigger, text_color, button_color, corner_roundness, hover_color, clicked_color)._widget
#
#         self._menu = Box(parent, width, height, corner_roundness=menu_corner_roundness, vertical_gap=0, alignment='start', side_alignment='start')
#
#         self._reloader2 = Reloader(dpi=parent.get_dpi(),
#                                    setup_properties={'command': command, 'options': options},
#                                    process_types={'command': 'super raw', 'options': 'super raw'},
#                                    default_values={'command': lambda: ..., 'options': [Option('First Option'), Option('Second Option', options=[Option('Sub option')])]},
#                                    property_types={'command': 'access', 'options': 'special'},
#                                    special_functions={'options': lambda v: self._restart_options(v)},
#                                    base='')
#
#         base = f"""QPushButton {{ background-color: {V}button_color{V}; font-family: {V}font{V}; font-size: {V}text_size{V}; color: {V}text_color{V}; border-radius: {V}corner_roundness{V}; }}
#         QPushButton:hover {{ background-color: {V}hover_color{V}; }}
#         QPushButton:pressed {{ background-color: {V}clicked_color{V}; }}"""
#
#         self._reloader = Reloader(parent.get_dpi(),
#                                   setup_properties  = {'hover_color': hover_color,   'clicked_color': clicked_color,    'command': command,     'corner_roundness': corner_roundness, 'button_color': button_color, 'text_color': text_color,   'text_size': text_size,     'font': font,         'text': text,              'parent': parent,   'width': width,          'height': height,},
#                                   process_types     = {'hover_color': 'color',       'clicked_color': 'color',          'command': 'super raw', 'corner_roundness': 'px-value',       'button_color': 'color',      'text_color': 'color',      'text_size': 'px-value',    'font': 'raw',        'text': 'raw',             'parent': None,     'width': 'px-value;int', 'height': 'px-value;int'},
#                                   default_values    = {'hover_color': 'litecrimson', 'clicked_color': 'delightcrimson', 'command': lambda: ..., 'corner_roundness': '0.03 inch',      'button_color': 'crimson',    'text_color': 'white',      'text_size': '0.15 inch',   'font': 'Verdana',    'text': 'Trilent Button.', 'parent': None,     'width': '1.2 inch',    'height': '0.40 inch'},
#                                   property_types    = {'hover_color': 'stylesheet',  'clicked_color': 'stylesheet',     'command': 'access',    'corner_roundness': 'stylesheet',     'button_color': 'stylesheet', 'text_color': 'stylesheet', 'text_size': 'stylesheet',  'font': 'stylesheet', 'text': 'special',         'parent': 'access', 'width': 'special',      'height': 'special'},
#                                   special_functions = {'text': base,  'width': lambda v: self._widget.setGeometry(self.x, self.y, v, self.height), 'height': lambda v: self._widget.setGeometry(self.x, self.y, self.width, v)},
#                                   base              = base)
#
#         self._optionWidgets = []
#
#         total_width = 0
#         total_height = 0
#
#         for option in self._reloader2.cp['options']:
#             menu = Menu(self._menu, *option.args)
#
#             total_width = max(total_width, menu.width)
#             total_height += menu.height
#
#             self._optionWidgets.append(menu)
#
#         if menu_open_side == 'bottom':
#             self._menu.set_position(self._menu.x, (self._menu.y + self._widget.height() + 1) * 2)
#         elif menu_open_side == 'right':
#             print(text)
#             self._menu.set_position((self._menu.x + self._widget.width() + 1) * 2, self._menu.y)
#
#         self._menu.set_size(total_width, total_height)
#         self._menu.hide()
#
#         self._state = 0
#
#     def show_menu(self):
#         self._menu.show()
#
#     def hide_menu(self):
#         self._menu.hide()
#
#     def _restart_options(self, new_options):
#         pass
