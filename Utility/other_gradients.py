
def samify(str1, str2, spacify=False):
    if spacify:
        str1 = str1.replace(' ', '⠀')

    if len(str1) < len(str2):
        str1 += ' ' * (len(str2) - len(str1))
    elif len(str1) > len(str2):
        str2 += ' ' * (len(str1) - len(str2))

    return str1, str2


def redundantify(string):
    return ' '.join(''.join(string).split()).rstrip()


def text_gradient(str1, str2, mode):
    spacify = False

    if " | " in mode:
        splitted = mode.split(' | ')
        spacify  = bool(splitted[-1].lower())
        mode     = ''.join(splitted[:-1])

    str1, str2 = samify(str1, str2, spacify)

    transitions = [str1]

    current = list(str1)
    goal = list(str2)
    center_index = len(str1) // 2
    size = len(str1) - 1

    if mode == 'wave' or mode == '':
        for i in range(max(len(str1), len(str2))):
            current[i] = goal[i]
            transitions.append(redundantify(current))
    elif mode == 'pulse':
        for i in range(max(len(str1), len(str2)) // 2):
            current[center_index - i] = goal[center_index - i]
            current[center_index + i] = goal[center_index + i]
            transitions.append(redundantify(current))
    elif mode == 'roll':
        for i in range(max(len(str1), len(str2))):
            current[size - i] = goal[size - i]
            transitions.append(redundantify(current))

    return transitions


if __name__ == '__main__':
    print(text_gradient('Test.', 'Secondary text.', 'pulse'))
