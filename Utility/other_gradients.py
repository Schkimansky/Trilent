# Unimplemented:

def wave_text_gradient(str1, str2):
    transitions = []
    return transitions


def pulse_text_gradient(str1, str2):
    transitions = []
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

