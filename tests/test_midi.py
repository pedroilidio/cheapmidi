from time import sleep
import mido

print('Available APIs:', mido.backend.module.get_api_names())

mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')
output_names = mido.get_output_names()
print('Available outputs:', output_names)
output = output_names[0]
print('Selected output:', output)

start_msg = mido.Message('note_on', note=60)
stop_msg = mido.Message('note_off', note=60)
port = mido.open_output(output)
port.send(start_msg)
sleep(2)
port.send(stop_msg)
port.close()

