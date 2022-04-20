import keyboard

print('Press a key on the keyboard you want to select.')
while (event := keyboard.read_event()).event_type == keyboard.KEY_UP: pass
selected_device = event.device
print(f'Selected device {selected_device}.')

last_event = None

while True:
    try:
        # Wait for the next event.
        event = keyboard.read_event()
        if event == last_event:
            continue  # Ignore continuous press.
        if event.device == selected_device:
            print("That's our KB!",
                  event.name, event.event_type, event.device)
        else:
            print("Not our KB, ignoring.",
                  event.name, event.event_type, event.device)
        last_event = event

    except KeyboardInterrupt:
        print('Exiting.')
        exit()
