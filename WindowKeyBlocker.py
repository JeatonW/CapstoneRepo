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



file = "C:/Users/joshu/Desktop/git/CapstoneRepo/Test Hotkey Files/equationsExamples.txt"
#file = "C:/Users/joshu/Desktop/git/CapstoneRepo/Test Hotkey FilesequationsExamples.txt"

tree = Reader.createCommandTree(file)
info = tree.solve()
HKList = tree.getHKList()
#print(f"Prints Hotkeys In List format{HKList}")
keys = formatKeys(HKList)
#print(f"Prints keys{repr(keys)}")
#HotkeyAction(keys)

def unpacktuple(commands):
    for i in commands:
        if i[0] == "Paste":
            PastInfo = i[1:]
        elif i[0] == "Highlight":
            HighlightInfo = i[1:]
        elif i[0] == "Start Cursor":
            StartCurosrInfo = i[1:]
        elif i[0] == "Move Cursor":
            MoveCursorInfo = i[1:]

        else:
            print("error with tuple")
    return PastInfo, HighlightInfo, StartCurosrInfo, MoveCursorInfo

    #past will type out the information in the past section
    # on hotket press, the information is pasted from the past tuple, we take the length of the past string and move the cursor back to the start of the
    #pasted string, then we read starcursorinfor to move the cursor to the first replacing variable. then you read the highligh info to get the length of
    # the first variable and highligh out to the end of its legth, then the user will type in what ever they want. after they replace it the cursor will
    #be at the end of it then we read the move cursor for the next variable and repeat, after every move cursor info we read highlight infor and keep
    # reapeating untill there is no more movecursor info.

    #need to unpack new tab data that oragnizes the highligh and move cursor info. 


P,H,S,M =  unpacktuple(info)
print(P)
print(H)
print(S)
print(M)