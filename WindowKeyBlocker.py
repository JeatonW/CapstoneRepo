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

def HotkeyAction(keys):
    def on_activate():
        print("keys have been pressed")

        example = "this will be typed out on hotkey press"
        c = keyboard.Controller()
        for char in example:
            c.tap(char)


    def for_canonical(f):
        return lambda k: f(l.canonical(k))




    hotkey = keyboard.HotKey(keyboard.HotKey.parse(keys),on_activate)
    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()


    '''
    def keyboard_listener():
        global listener
        def on_press(key):
            print('on press', key)

        def on_release(key):
            print('on release', key)
            if key == keyboard.Key.esc:
                return False 
     
        def win32_event_filter(msg, data):
            #checks if message is the key press
            blocked =["84,69,83"]
            if (msg == 257 or msg == 256) and (data.vkCode == 84 or data.vkCode == 69 or data.vkCode == 83): 
                print(msg,data)
                print("Suppressing F1 up")
                listener._suppress = True
               
            else:
                listener._suppress = False
            return True
                
        return keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            win32_event_filter=win32_event_filter,
            suppress=False
        )
    
    listener = keyboard_listener()

    with listener as ml:
        ml.join() 
    '''