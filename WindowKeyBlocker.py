from pynput import keyboard
import pynput
import Reader

#this program is responsible for just blocking the spevified windows keys and allowing the combo on keys
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



#file = "C:/Users/joshu/Desktop/git/CapstoneRepo/Test Hotkey Files/equationsExamples.txt"
file = "C:/Users/joshu/OneDrive/Documents/GitHub/CapstoneRepo/Test Hotkey Files/pseudolang.txt"

tree = Reader.createCommandTree(file)
info = tree.solveAndPrint()
HKList = tree.getHKList()

print(f"Prints Hotkeys In List format{HKList}")
keys = formatKeys(HKList)
print(f"Prints keys{repr(keys)}")
#HotkeyAction(keys)

print(info)