import argparse
import copy
import yaml
import keyboard as kb
import mido
from parse import parse_keymap


class EventHandler:
    def __init__(self, midi_out, key_map, selected_device=None):
        self.selected_device = selected_device
        self.last_event = None
        self.midi_out = midi_out
        self.key_map = key_map
        self.transpose = 0
        self.state = {}

    def handle_event(self, event):
        if self.selected_device is None:
            raise RuntimeError("No device selected.")
        if event == self.last_event:
            return  # Ignore continuously holding key down.

        self.last_event = event

        if event.device != self.selected_device:
            return  # Ignore different keyboard.

        instruction = self.key_map.get(event.scan_code)

        if instruction is None:
            print(f'Unmapped key {event.name!r} ({event.scan_code})')
            return
        if event.event_type == kb.KEY_DOWN:
            message = copy.copy(instruction.down)
            if instruction.relative:  # FIXME: cannot toggle just by adding
                # TODO: default should be 64 (not 0) for continuous controllers
                message.value += self.state.get(event.scan_code, 0)
                self.state[event.scan_code] = message.value
        # elif event.event_type == kb.KEY_UP:
        else:
            message = copy.copy(instruction.up)

        if message is None:
            return
        if message.type == 'transpose':
            print(
                "Key {0.name} {0.scan_code} {0.event_type}.".format(event),
                 "Transposition changed from",
                 self.transpose,
                 end=' to ',
            )
            self.transpose += message.semitones
            print(self.transpose, '.')
            return
        if message.type in ('note_on', 'note_off'):
            message.note += self.transpose

        self.midi_out.send(message)

        print(
            "Key {0.name} {0.scan_code} {0.event_type}. Sent".format(event),
            message
        )

    def prompt_device_selection(self):
        print('Press a key on the keyboard you want to select.')
        while (event := kb.read_event()).event_type == kb.KEY_DOWN: pass
        selected_device = event.device
        print(f'Selected device {selected_device}.')
        self.selected_device = selected_device
        return selected_device


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('map', type=argparse.FileType('r'))
    args = argparser.parse_args()

    key_map = parse_keymap(yaml.safe_load(args.map))

    mido.set_backend('mido.backends.rtmidi/UNIX_JACK')
    midi_out = mido.open_output('CheapMIDI', virtual=True)

    handler = EventHandler(key_map=key_map, midi_out=midi_out)
    handler.prompt_device_selection()
    kb.hook(handler.handle_event)

    try:
        kb.wait()
    except KeyboardInterrupt:
        print('Exiting.')
        exit()


if __name__ == '__main__':
    main()
