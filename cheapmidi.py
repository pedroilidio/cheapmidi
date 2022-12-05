from functools import partial
from itertools import cycle
import keyboard as kb
import mido

KEY_NOTE = 69

DEFNOTEMAP = {
    'a': 60, 's': 61, 'd':62, 'f':63, 'g':63,
}

DEF_KBLAYOUT = (
    'zxcvbnm,.;',
    'asdfghjklç',
    'qwertyuiop',
    '1234567890-=',
)

scale_map = dict(
    D = ('major diatonic', [2, 2, 1, 2, 2, 2, 1]),
    d = ('minor diatonic', [2, 1, 2, 2, 1, 2, 2]),
    p = ('minor pentatonic', [3, 2, 2, 3, 2]),
    pb = ('minor penta-blues', [3, 2, 1, 1, 3, 2]),
)

ex = tuple(scale_map.values())[0]  # sample scale

scale_help = (
    '\nEnter one of following codes:\n\n  '
    '\n  '.join(ID + ' = ' + name
        for ID, (name, _) in scale_map.items()) +
    '\n\nAlternatively, enter interval sequence. Example:\n  '
    f'{" ".join(map(str, ex[1]))}\nfor selecting {ex[0]}.'
    '\n\n Answer: '
)


def generate_note_map(
    scale_sig=scale_map['pb'][1],
    key_note=KEY_NOTE,
    kblayout=DEF_KBLAYOUT,
    from_key=False,
):
    # If from_key, scale_sig is a list of integers representing
    # intervals in semitones from the key_note. Ex.:
    # diatonic scale's scale_sig is [2, 4, 5, 7, 9, 11]
    # Else, it is just the list of intervals in semitones.
    # Ex.: diatonic signature is [2,2,1,2,2,2,1]
    note_map = {}

    if from_key:
        scale_sig = [0] + scale_sig + [12]
        scale_sig = [
            scale_sig[i]-scale_sig[i-1]
            for i in range(1, len(scale_sig))
        ]

    for i in range(len(kblayout)):
        note_map.update({
            kblayout[i][0] : key_note + 12 * (i-1)
        })
        cyc = cycle(scale_sig)

        for j in range(1, len(kblayout[0])):
            note_map.update({
                kblayout[i][j]: note_map[kblayout[i][j-1]] + next(cyc)
            })

    return note_map


def print_notes(event, notemap=None):
    notemap = notemap or DEFNOTEMAP
    print(notemap.get(event.name, 'não tem'))


def send_midi(event, midiout, notemap=None):
    notemap = notemap or DEFNOTEMAP
    note = notemap.get(event.name)
    if note:
        on_off = 'note_on' if event.event_type is kb.KEY_DOWN else 'note_off'
        midiout.send(mido.Message(on_off, note=note))


class EventHandler:
    def __init__(self, selected_device=None):
        self.selected_device = selected_device
        self.last_event = None
        self.callback = None

    def set_callback(self, callback, **kwargs):
        self.callback = partial(callback, **kwargs)

    def handle_event(self, event):
        if self.selected_device is None:
            raise RuntimeError("No device selected.")
        if self.callback is None:
            raise RuntimeError("No callback function was set.")
        if event == self.last_event:
            return  # Ignore continuously holding key down.
        if event.device == self.selected_device:
            self.callback(event)
        #else:
            #print(" Not our KB, ignoring.")

        #print(event.name, event.event_type, event.device, event.scan_code)
        self.last_event = event

    def prompt_device_selection(self):
        print('Press a key on the keyboard you want to select.')
        while (event := kb.read_event()).event_type == kb.KEY_DOWN: pass
        selected_device = event.device
        print(f'Selected device {selected_device}.')
        self.selected_device = selected_device
        return selected_device


def main():
    handler = EventHandler()
    handler.prompt_device_selection()
    output = mido.get_output_names()[0]
    print('Selected MIDI output:', output)
    midiout = mido.open_output(output)
    handler.set_callback(
        send_midi,
        midiout=midiout,
        notemap=generate_note_map()
    )
    kb.hook(handler.handle_event)

    try:
        kb.wait()
    except KeyboardInterrupt:
        print('Exiting.')
        exit()


if __name__ == '__main__':
    main()
=======
from time import sleep
import gi
import mido

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file('cheapmidi.glade')

mido.set_backend('mido.backends.rtmidi/UNIX_JACK')
midi_out = mido.open_output('CheapMIDI', virtual=True)

def print_hi(button):
    print('hi!')

def send_note(b):
    print('sending note')
    midi_out.send(mido.Message('note_on', note=72))
    sleep(1)
    midi_out.send(mido.Message('note_off', note=72))

builder.connect_signals({
    'sendNote': send_note,
    'onDestroy': Gtk.main_quit,
    'quit': Gtk.main_quit,
})

builder.get_object('main_window').show_all()
Gtk.main()
