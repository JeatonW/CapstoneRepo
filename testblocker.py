from pynput import keyboard
import pynput

#function used to format the keys to send to the Hotkeyfunction of 
def formatKeys(hotkeys):
    KeysToBeFormated = ["shift","ctrl_l","alt_l","ctrl_r","alt_r"]
    KeyFinal = ""
    for hotkey in hotkeys:
        for keys in hotkey:
            split = str(keys).split(".")[-1]
            if split in KeysToBeFormated:
                Format = f"<{split}>"
                KeyFinal+=Format

            KeyFinal += split
            KeyFinal += "+"
    KeyFinal = KeyFinal[:-1]
    return KeyFinal


#def HotkeyAction(keys):
def on_activate():
    print("Keys have been pressed")

    example = "This will be typed out on hotkey press"
    c = keyboard.Controller()
    for char in example:
        c.tap(char)

def on_press(key):
    pass  # Modify as needed

def on_release(key):
    pass  # Modify as needed

def win32_event_filter(msg, data):
    blocked = ["84,69,83"]  # List of blocked key codes
    if (msg == 257 or msg == 256) and (data.vkCode == 84 or data.vkCode == 69 or data.vkCode == 83):
        print(msg, data)
        print("Suppressing F1 up")
        listener._suppress = True
    else:
        listener._suppress = False
    return True

# Define the hotkey as '<ctrl>+<alt>+t'
hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<alt>+t'), on_activate)

# Define the listener with the specified functions and filters
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    win32_event_filter=win32_event_filter,
    suppress=False
)

# Register the hotkey
with keyboard.GlobalHotKeys({'<ctrl>+<alt>+t': hotkey}) as h:
    h.join()  # Wait for the listener to finish