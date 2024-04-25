import Reader
import time
import pyautogui
import keyboard

#this program is responsible for just blocking the spevified windows keys and allowing the combo on keys
#function used to format the keys to send to the Hotkeyfunction of 
def formatKeys(hotkeys):
    KeysToBeFormated = ["shift","ctrl_l","alt_l","ctrl_r","alt_r"]
    KeyFinal = ""
    for hotkey in hotkeys:
        for keys in hotkey:
            split = str(keys).split(".")[-1]
            if split.lower() in KeysToBeFormated:
                string = split.lower()
                Format = f"{string.split("_")[0] if string.split("_")[1] == "l" else None }"
                KeyFinal+=Format
            else:
                KeyFinal += split.lower()
            KeyFinal += "+"
    KeyFinal = KeyFinal[:-1]
    return KeyFinal

def HotkeyAction(keys,PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab):
    esc_pressed = False  # Flag variable to track if 'esc' key is pressed
    tabindex = 0
    def my_function(PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab):
        print("HotKeyPressed")
        time.sleep(.5)
        print(PastInfo)
        print(HighlightInfo)
        print(StartCurosrInfo)
        print(mouseInfo)
        print(MoveAfterTab)
        print(HighlightonTab)
        pyautogui.typewrite(PastInfo[0])
        time.sleep(.5)
        for x in range((len(PastInfo[0]))- int(StartCurosrInfo[0])):
            pyautogui.press("left",interval=.01)
        
        keyboard.press('left shift')
        time.sleep(.5)
        keyboard.press('right shift')
        time.sleep(.5)
        pyautogui.press("right",presses=int(HighlightInfo[0]),interval=.01)
        time.sleep(.5)
        keyboard.release('right shift')
        time.sleep(.5)
        keyboard.release('left shift')
        time.sleep(.5)

        #pyautogui.press('shiftright')


        print(keyboard.is_pressed('right shift'))
        print("selection done")
        keyboard.add_hotkey('tab',lambda:tab_pressed(MoveAfterTab,HighlightonTab),suppress=True)
        print("tab as been added to hotkey")
        keyboard.release('right shift')
        print(keyboard.is_pressed('right shift'))
        #for x in MoveAfterTab:
            #for NumberOfPresses in range(int(x[0])): 
            #    pyautogui.press("right",interval=.01)
            
    def my_exit():
        global esc_pressed
        print("Quitting...")
        esc_pressed = True
    def tab_pressed(MoveAfterTab,HighlightonTab):
        nonlocal tabindex
        print("tab pressed")
        for x in range(int(MoveAfterTab[tabindex][0])):
            pyautogui.press("right",interval=.01)
        tabindex+=1

    # Register hotkeys for 'ctrl+alt+h' and 'esc'
    keyboard.add_hotkey(keys, lambda: my_function(PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab))
    keyboard.add_hotkey('esc', my_exit)
    

    try:
        while True:
            
            keyboard.wait('esc')
            break  # Exit the while loop when 'esc' is pressed
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully
    finally:
        keyboard.unhook_all()  # Ensure hotkeys are unhooked before exiting 


#file = "C:/Users/joshu/Desktop/git/CapstoneRepo/Test Hotkey Files/equationsExamples.txt"
file = "C:/Users/joshu/Documents/GitHub/CapstoneRepo/Test Hotkey Files/pseudolang2.txt"

tree = Reader.createCommandTree(file)
info = tree.solve()
HKList = tree.getHKList()
#print(f"Prints Hotkeys In List format{HKList}")
keys = formatKeys(HKList)
#print(f"Prints keys{repr(keys)}")



def unpacktuple(commands):
    tabInfo = []
    for i in commands:
        #print(f"unpacked Commands:{i}")
        if i[0] == "Paste":
            PastInfo = i[1:]
        elif i[0] == "Highlight":
            HighlightInfo = i[1:]
        elif i[0] == "Start Cursor":
            StartCurosrInfo = i[1:]
        elif i[0] == "Key Press":
            if i[1] == "M1":
                mouseInfo = i[2:]
            elif i[1] == "TAB":
                tabInfo.append(i[3:][0])
        else:
            print("error with tuple")
    return PastInfo, HighlightInfo, StartCurosrInfo, mouseInfo,tabInfo

    #past will type out the information in the past section
    # on hotket press, the information is pasted from the past tuple, we take the length of the past string and move the cursor back to the start of the
    #pasted string, then we read starcursorinfor to move the cursor to the first replacing variable. then you read the highligh info to get the length of
    # the first variable and highligh out to the end of its legth, then the user will type in what ever they want. after they replace it the cursor will
    #be at the end of it then we read the move cursor for the next variable and repeat, after every move cursor info we read highlight infor and keep
    # reapeating untill there is no more movecursor info.

    #need to unpack new tab data that oragnizes the highligh and move cursor info. 

def processTabs(tabList):
    movecursorInfo = []
    highlightInfoTab = []
    for tabs in tabList:
        #print(tabs)
        #reads the Move Cursor info
        movecursorInfo.append(tabs[0][1:])

        #reads the highlight action after a tab press
        highlightInfoTab.append(tabs[1][1:])

    return movecursorInfo,highlightInfoTab


PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,tabInfo =  unpacktuple(info)


MoveAfterTab,HighlightonTab = processTabs(tabInfo)

#print(MoveAfterTab)
#print(HighlightonTab)


HotkeyAction(keys,PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab)