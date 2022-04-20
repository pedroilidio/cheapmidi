import keyboard as kb


class EventHandler:
    def __init__(self, selected_device=None):
        self.selected_device = selected_device
        self.last_event = None

    def handle_event(self, event):
        if self.selected_device is None:
            raise RuntimeError("No device selected.")
        if event == self.last_event:
            return  # Ignore continuously holding key down.
        if event.device == self.selected_device:
            print(" That's our KB!")
        else:
            print(" Not our KB, ignoring.")

        print(event.name, event.event_type, event.device, event.scan_code)
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
    kb.hook(handler.handle_event)

    try:
        kb.wait()
    except KeyboardInterrupt:
        print('Exiting.')
        exit()


if __name__ == '__main__':
    main()
