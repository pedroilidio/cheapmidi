from dataclasses import dataclass
# from enum import StrEnum, auto  # TODO(Python 3.11)
from enum import Enum
from mido import Message, MetaMessage
from mido.midifiles.meta import MetaSpec, add_meta_spec


# TODO(Python 3.11)
# class InstructionType(StrEnum):
#     NOTE = auto()
#     SWITCH = auto()
#     BUTTON = auto()
#     TRANSPOSE = auto()
#     RAW = auto()


@dataclass
class Instruction:
    up: Message | None = None
    down: Message | None = None
    relative: bool = False


from mido.midifiles.meta import MetaSpec, add_meta_spec

class MetaSpec_transpose(MetaSpec):
    type_byte = 0xf0
    attributes = ['semitones']
    defaults = [0]

    def decode(self, message, data):
        # Interpret the data bytes and assign them to attributes.
        (message.r, message.g, message.b) = data

    def encode(self, message):
        # Encode attributes to data bytes and
        # return them as a list of ints.
        return [message.r, message.g, message.b]

    def check(self, name, value):
        # (Optional)
        # This is called when the user assigns
        # to an attribute. You can use this for
        # type and value checking. (Name checking
        # is already done.
        #
        # If this method is left out, no type and
        # value checking will be done.

        if not isinstance(value, int):
            raise TypeError('{} must be an integer'.format(name))

        if not -127  <= value <= 127:
            raise TypeError('{} must be in range -127..127'.format(name))

add_meta_spec(MetaSpec_transpose)

def parse_instruction(key: int, instruction: dict) -> dict[str, Message]:
    if instruction['type'] == 'note':
        instruction = instruction.copy()
        del instruction['type']
        return Instruction(
            down=Message('note_on', **instruction),
            up=Message('note_off', **instruction),
        )
    elif instruction['type'] == 'button':
        control = instruction.get('control', key)
        return Instruction(
            down=Message('control_change', control=control, value=127),
            up=Message('control_change', control=control, value=0),
        )
    elif instruction['type'] == 'switch':
        control = instruction.get('control', key)
        return Instruction(
            down=Message('control_change', control=control, value=127),
            relative=True,
        )
    elif instruction['type'] == 'raw':
        return Instruction(
            up=instruction.get('up') and Message(**instruction['up']),
            down=instruction.get('down') and Message(**instruction['down']),
            relative=instruction.get('relative', False),
        )
    elif instruction['type'] == 'transpose':
        return Instruction(
            down=MetaMessage('transpose', semitones=instruction['semitones'])
        )
    else:
        raise ValueError(f'Unknown instruction type {instruction["type"]!r}')


def parse_keymap(map: dict):
    return {k: parse_instruction(k, v) for k, v in map.items()}

