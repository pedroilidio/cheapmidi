# Can`t differentiate input sources. We'll be using the keyboard module.

from pynput import keyboard

def on_press(key):
    try:
        print(key)
        breakpoint()
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print(repr(key), type(key))
    print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #     # Stop listener
    #     return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print('Exiting.')
        exit()
