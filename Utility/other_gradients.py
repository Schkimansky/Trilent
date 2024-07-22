
def wave_text_gradient(str1, str2):
    len1, len2 = len(str1), len(str2)
    max_len = max(len1, len2)

    if len1 < max_len:
        str1 += ' ' * (max_len - len1)
    elif len2 < max_len:
        str2 += ' ' * (max_len - len2)

    transitions = [str1]

    list1 = list(str1)
    list2 = list(str2)

    for i in range(max_len):
        if list1[i] != list2[i]:
            list1[i] = list2[i]
            transitions.append(' '.join(''.join(list1).split()))

    for i in range(len(transitions)):
        if transitions[i] == ' ':
            transitions.pop(i)
        transitions[i] = transitions[i].rstrip()

    return transitions


def pulse_text_gradient(str1, str2):

    return transitions


def text_gradient(text1, text2, steps, mode):
    if mode == '':
        mode = 'wave'

    if mode == 'wave' or mode == '':
        return wave_text_gradient(text1, text2)
    if mode == 'pulse':
        return pulse_text_gradient(text1, text2)


if __name__ == '__main__':
    print(text_gradient('Thats nice', 'wow', 3, ''))

