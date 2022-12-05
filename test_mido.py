import mido

print(mido.backend.module.get_api_names())
mido.set_backend('mido.backends.rtmidi/UNIX_JACK')
# mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')

# inport = mido.open_input('ChepMIDIin', virtual=True)
outport = mido.open_output('CheapMIDI', virtual=True)
ports = mido.get_ioport_names()
print('ioports:', ports)

# Works for ALSA
# outport = mido.open_output(ports[0])
# inport = mido.open_input(ports[0])

outport.send(mido.Message('note_on', note=72))
while True:
    print('message sent')
    outport.send(mido.Message('note_on', note=72))
    sleep(0.5)
    outport.send(mido.Message('note_off', note=72))
    sleep(2)
exit()
