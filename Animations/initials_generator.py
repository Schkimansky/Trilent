
def generate_initials(name, end_value, widget):
    if name in ['x', 'y']:
        start_value = getattr(widget, name)
        end_value = widget._reloader.alternate_process('px-value;int', end_value)
        return start_value, end_value, 'px-value;int'
    elif name == 'text':
        start_value = widget.get(name)
        return start_value, end_value, 'text'
    elif isinstance(end_value, str) and end_value.__contains__(' -> '):
        start_value = widget.get(name)
        if not start_value.__contains__(' -> '):
            start_value = f"{start_value} -> " * end_value.count(' -> ')
            start_value = start_value.removesuffix(' -> ')

        return start_value, end_value, 'gradient color'
    else:
        start_value = widget._reloader.process(name, widget._reloader.cp[name])
        end_value = widget._reloader.process(name, end_value)
        type = widget._reloader.initial_parameters['process_types'][name]
        return start_value, end_value, type

