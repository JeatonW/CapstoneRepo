import Reader
import time
import pyautogui
import keyboard
from win32api import GetKeyState 
from win32con import VK_NUMLOCK

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
                Format = f"{string.split('_')[0] if string.split('_')[1] == 'l' else None }"
                KeyFinal+=Format
            else:
                KeyFinal += split.lower()
            KeyFinal += "+"
    KeyFinal = KeyFinal[:-1]
    return KeyFinal

def HotkeyAction(keys,PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab):
    #adds a flag and tabindex to keep track of the escape key to exit the program and to keep track of tabs,also a numlock flag
    esc_pressed = False
    tabindex = 0
    wasNumlockDisabled = False

    def my_function(PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab):
        #buffer time just in case, might cause errors if no buffer
        time.sleep(.5)

        #we check the state of the numlock key, as is causes weird interactions with the shift keys, if the numlock is on we turn it off and take a note that it was done
        if GetKeyState(VK_NUMLOCK) == 1:
            pyautogui.press('numlock')
            wasNumlockDisabled = True

        #reads from the past info of the hotkey and moves it to starting position
        keyboard.write(PastInfo[0])
        pyautogui.press("left",presses=(len(PastInfo[0]))- int(StartCurosrInfo[0]),interval=.01)
        
        #selects the initial variable
        keyboard.press('left shift')
        keyboard.press('right shift')
        pyautogui.press("right",presses=int(HighlightInfo[0]),interval=.01)
        keyboard.release('right shift')
        keyboard.release('left shift')

        #temporarly adds tab to a hot key to call a function to hook it and read from the rest of the variables
        keyboard.add_hotkey('tab',lambda:tab_pressed(MoveAfterTab,HighlightonTab,wasNumlockDisabled),suppress=True,trigger_on_release=True)

    #this function is a hot key for the esc key to exit the program
    def my_exit():
        global esc_pressed
        print("Quitting...")
        esc_pressed = True

    #this function is used to move the key cursor to the proper location after initial selection
    def tab_pressed(MoveAfterTab,HighlightonTab,wasNumlockDisabled):
        nonlocal tabindex

        #checks the length of the tab variable to make sure to only use this if there are tabs left, else we unhook tab to free is from the program.
        if tabindex < len(MoveAfterTab):
            time.sleep(.5)
            pyautogui.press("right",presses=int(MoveAfterTab[tabindex][0]),interval=.01)

            keyboard.press('left shift')
            keyboard.press('right shift')
            pyautogui.press("right",presses=int(HighlightonTab[tabindex][0]),interval=.01)
            keyboard.release('right shift')
            keyboard.release('left shift')
            tabindex+=1
        #after all the tabs have been gone through it unhooks tab and checks if we diabled numlock at the start and will re-enable it 
        else:
            keyboard.remove_hotkey('tab')
            if wasNumlockDisabled:
                pyautogui.press('numlock')  

    #initial registaion of our hotkeys and our esc to quit the program
    #the only known limitaion i know of right now is that for some reason adding suppress=True and trigger_on_release=True do not function properly in this area, even though it works up top
    keyboard.add_hotkey(keys, lambda: my_function(PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab))
    keyboard.add_hotkey('esc', my_exit)
    

    #a try funtion that will hold a subprocces and see if esc was pressed, if Ctrl+c is click it catches the exception and quits the program and unhooks all keys
    try:
        while True:
            keyboard.wait('esc')
            break
    except KeyboardInterrupt:
        pass  
    finally:
        keyboard.unhook_all()

#unpacks the tuples from the main program,
#KNOWN ISSUE: some tuples get left with weird commas at the end, will come pack to unpack more effectivly
def unpacktuple(commands):
    tabInfo = []
    for i in commands:
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

#unpacks the second layer of tuples labeled as tab
#same issue as above
def processTabs(tabList):
    movecursorInfo = []
    highlightInfoTab = []
    for tabs in tabList:
        movecursorInfo.append(tabs[0][1:])
        highlightInfoTab.append(tabs[1][1:])

    return movecursorInfo,highlightInfoTab



#KNOW ISSUE: eventually this should read the file from the sys.argv cmd line
#file = "C:/Users/joshu/Desktop/git/CapstoneRepo/Test Hotkey Files/pseudolang2.txt"
file = "C:/Users/joshu/Documents/GitHub/CapstoneRepo/Test Hotkey Files/pseudolang2.txt"

#creates the tree, solves it, takes the keys, formats keys, and takes the return of tree.solve() and sends them to be unpacked
tree = Reader.createCommandTree(file)
info = tree.solve()
HKList = tree.getHKList()
keys = formatKeys(HKList)

#unpacks the tuples and unpacks the tabs information to be stored in their individual variables for processing
PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,tabInfo =  unpacktuple(info)
MoveAfterTab,HighlightonTab = processTabs(tabInfo)

#starts the main program
#HotkeyAction(keys,PastInfo,HighlightInfo,StartCurosrInfo,mouseInfo,MoveAfterTab,HighlightonTab)


#below is a snipit of code that will return the active window
'''
import pygetwindow as gw
def get_active_window_title():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title
    else:
        return "No active window found"

time.sleep(10)
active_window_title = get_active_window_title()
print("Active Window Title:", active_window_title)
'''