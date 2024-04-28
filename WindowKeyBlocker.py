import Reader
import time
import pyautogui
import keyboard
from win32api import GetKeyState 
from win32con import VK_NUMLOCK,VK_SHIFT,VK_MENU,VK_CONTROL

def cSharpWrite(keys):
    with open("cSharp.txt","w") as f:
        for key in keys:
            f.write(key+"\n")

#this program is responsible for just blocking the spevified windows keys and allowing the combo on keys
#function used to format the keys to send to the Hotkeyfunction of 
def formatKeys(hotkeys):
    KeysToBeFormated = ["CTRL_L","CTRL_R","ALT_L","ALT_R","SHIFT_L","SHIFT_R"]
    finalList = []
    for keyset in hotkeys:
        KeyFinal = ""
        for key in keyset:
            if key in KeysToBeFormated:
                keysplit = key.split('_')
                if keysplit[1] == "L":
                    side = "left"
                else:
                    side = "right"
                KeyFinal+= (side+" "+keysplit[0].lower()+"+")
            else:
                KeyFinal+= key.lower()

        #checks for a plus at the end
        if KeyFinal[-1] == "+":
            KeyFinal = KeyFinal[:-1]

        finalList.append(KeyFinal)
    cSharpWrite(finalList)
    return finalList

def HotkeyAction(keys,PasteInfo,StartCurosrInfo,HighlightInfo,tabInfo):
    #adds a flag and tabindex to keep track of the escape key to exit the program and to keep track of tabs,also a numlock flag
    esc_pressed = False
    tabindex = 0
    wasNumlockDisabled = False

    def my_function(PasteInfo,HighlightInfo,startcurosrInfo,tabInfo):
        
        print(PasteInfo,HighlightInfo,startcurosrInfo,tabInfo)
        
        #buffer time just in case, might cause errors if no buffer
        time.sleep(.5)

        if PasteInfo != []:
            #reads from the past info of the hotkey and moves it to starting position
            keyboard.write(PasteInfo)

        if (PasteInfo!=[])and(startcurosrInfo!=[]):
            print(len(PasteInfo[0]))
            print(int(startcurosrInfo[0]))
            print((len(PasteInfo[0])) - int(startcurosrInfo[0]))
            pyautogui.press("left",presses=(len(PasteInfo[0])) - int(startcurosrInfo[0]),interval=.01)
        
        #we check the state of the numlock key, as is causes weird interactions with the shift keys, if the numlock is on we turn it off and take a note that it was done
        if GetKeyState(VK_NUMLOCK) == 1:
            pyautogui.press('numlock')
            wasNumlockDisabled = True
        else:
            wasNumlockDisabled = False

        if HighlightInfo != []:
            #selects the initial variable
            keyboard.press('left shift')
            keyboard.press('right shift')
            pyautogui.press("right",presses=int(HighlightInfo[0]),interval=.01)
            keyboard.release('right shift')
            keyboard.release('left shift')

        if tabInfo != []:
            #temporarly adds tab to a hot key to call a function to hook it and read from the rest of the variables
            keyboard.add_hotkey('tab',lambda:tab_pressed(tabInfo,wasNumlockDisabled),suppress=True, trigger_on_release=True)
        

    #this function is a hot key for the esc key to exit the program
    def my_exit():
        global esc_pressed
        print("Quitting...")
        esc_pressed = True

    #this function is used to move the key cursor to the proper location after initial selection
    def tab_pressed(tabInfo,wasNumlockDisabled):
        nonlocal tabindex
        #checks the length of the tab variable to make sure to only use this if there are tabs left, else we unhook tab to free is from the program.
        if tabindex < len(tabInfo):
            time.sleep(.5)
            pyautogui.press("right",presses=int(tabInfo[tabindex][0]),interval=.01)

            keyboard.press('left shift')
            keyboard.press('right shift')
            pyautogui.press("right",presses=int(tabInfo[tabindex][1]),interval=.01)
            keyboard.release('right shift')
            keyboard.release('left shift')
            tabindex+=1
        #after all the tabs have been gone through it unhooks tab and checks if we diabled numlock at the start and will re-enable it 
        else:
            tabindex = 0
            print("unhooking tab")
            keyboard.remove_hotkey('tab')
            if wasNumlockDisabled:
                pyautogui.press('numlock')  

    #initial registaion of our hotkeys and our esc to quit the program
    #the only known limitaion i know of right now is that for some reason adding suppress=True and trigger_on_release=True do not function properly in this area, even though it works up top
    for key in keys:
        keyboard.add_hotkey(key, lambda p = PasteInfo[keys.index(key)], h = HighlightInfo[keys.index(key)],s = StartCurosrInfo[keys.index(key)],t = tabInfo[keys.index(key)]: my_function(p,h,s,t))
    

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
def unpacktuple(trees):
    #stores the solved trees
    hotkey = []

    #master list for every hotkey
    paste = []
    startCursor = []
    initialHighligh = []
    tab = []

    #solves tree and puts into a info list
    for tree in trees:
        hotkey.append(tree.solve())

    #steps into each tree
    for info in hotkey:
        #temps to be appeneded to master lists
        #this is used to line up with the index of the hotkey.
        pasteInfo = []
        startCursorInfo = []
        initialHighlighInfo = []

        #for of [move,highlight]
        numberofTabs = []

        #steps into all the info for each tree, and appends the corisponding keyword with its data type list
        for keyword in info:
            if keyword[0] == "Paste":
                pasteInfo.append(keyword[1])
            if keyword[0] == "Start Cursor":
                startCursorInfo.append(keyword[1])
            if keyword[0] == "Highlight":
                initialHighlighInfo.append(keyword[1])
            if keyword[0] == "Key Press":
                if keyword[1] == "TAB":
                    #trims the tab section
                    _tab = keyword[3:][0]
                    for action in _tab:
                        if action[0] == "Move Cursor":
                            move = action[1]
                        if action[0] == "Highlight":
                            highlight = action[1]
                    #packs the tab pair into its own list, that gets appended to the currnet hotekys tab list
                    numberofTabs.append([move,highlight])
                    
        tab.append(numberofTabs)
        paste.append(pasteInfo)
        startCursor.append(startCursorInfo)
        initialHighligh.append(initialHighlighInfo)

    print(f"{paste}\n{startCursor}\n{initialHighligh}\n{tab}")
    return paste,startCursor,initialHighligh,tab


#KNOW ISSUE: eventually this should read the file from the sys.argv cmd line
#file = "C:/Users/joshu/Desktop/git/CapstoneRepo/Test Hotkey Files/pseudolang2.txt"
file = "C:/Users/joshu/Documents/GitHub/CapstoneRepo/Test Hotkey Files/pseudolang2.txt"

#creates the tree, solves it, takes the keys, formats keys, and takes the return of tree.solve() and sends them to be unpacked
tree = Reader.createCommandTree(file)
HKList = tree.getHKList()

keylist = []
treelist = []
for hotkey in HKList:
    keylist.append(hotkey[0])
    treelist.append(hotkey[1])

keys = formatKeys(keylist) 

p,s,i,t = unpacktuple(treelist)

print(keys)
#starts the main program
HotkeyAction(keys,p,s,i,t)
