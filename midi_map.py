#! /bin/python
from itertools import cycle

KEY_NOTE = 69

scale_map = dict(
    D = ('major diatonic', [2, 2, 1, 2, 2, 2, 1]),
    d = ('minor diatonic', [2, 1, 2, 2, 1, 2, 2]),
    p = ('minor pentatonic', [3, 2, 2, 3, 2]),
    pb = ('minor penta-blues', [3, 2, 1, 1, 3, 2]),
)

ex = tuple(scale_map.values())[0]  # sample scale

scale_help = (
    '\nEnter one of following codes:\n\n  ' +
    '\n  '.join(ID + ' = ' + name
        for ID, (name, _) in scale_map.items()) +

    '\n\nAlternatively, enter interval sequence. Example:\n  '
    f'{" ".join(map(str, ex[1]))}\nfor selecting {ex[0]}.'
    '\n\n Answer: '
)


def generate_note_map(scale_sig, key_note, from_key=False):
    # If from_key, scale_sig is a list of integers representing
    # intervals in semitones from the key_note. Ex.:
    # diatonic scale's scale_sig is [2, 4, 5, 7, 9, 11]
    # Else, it is just the list of intervals in semitones.
    # Ex.: diatonic signature is [2,2,1,2,2,2,1]

    if from_key:
        scale_sig = [0] + scale_sig + [12]
        scale_sig = [scale_sig[i]-scale_sig[i-1] for i in range(1, len(scale_sig))]

    else:
        scale_sig = scale_sig

    # std_layout = [
    #     'zxcvbnm,.;',
    #     'asdfghjklç',
    #     'qwertyuiop',
    #     '1234567890-=',
    # ]
    std_layout = [
        list(range(44, 54)) + [89],
        list(range(30, 41)) + [43],
        list(range(16, 28)),
        list(range(2, 14)),
    ]

    note_map = {}
    for i in range(len(std_layout)):
        cyc = cycle(scale_sig)

        note_map[std_layout[i][0]] = key_note + 12 * (i-1)
        for j in range(1, len(std_layout[i])):
            note_map[std_layout[i][j]] = note_map[std_layout[i][j-1]] + next(cyc)

    return note_map
