import Reader
import time
import pyautogui
import keyboard
from win32api import GetKeyState 
from win32con import VK_NUMLOCK,VK_SHIFT,VK_MENU,VK_CONTROL
import sys

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
    return finalList


def HotkeyAction(keys,Info):
    #adds a flag and tabindex to keep track of the escape key to exit the program and to keep track of tabs,also a numlock flag
    esc_pressed = False
    wasNumlockDisabled = False
    #a list that inserts a true value for each home press, so when you stay on a certain line. it will no longer press home.
    def my_function(Info):
        time.sleep(.5) #buffer time just in case, might cause errors if no buffer
        lineNumber = 0
        homePressedOnSameLine = []
        if GetKeyState(VK_NUMLOCK) == 1:
            pyautogui.press('numlock')
            wasNumlockDisabled = True
        else:
            wasNumlockDisabled = False


        for keyword in Info:
            print(keyword)
            print(f"Line:{lineNumber}")
            if keyword[0] == "Paste":
                if r"\n" == keyword[1][-2:]:
                    lineNumber += 1
                    keyboard.write(keyword[1][:-2])
                    keyboard.press("enter")
                else:
                    keyboard.write(keyword[1])
            
            if keyword[0] == "Start Cursor":
                lineNumber,homePressedOnSameLine = moveline(keyword[1],keyword[2],lineNumber,homePressedOnSameLine)

            if keyword[0] == "Highlight":
                #selects the initial variable
                keyboard.press('left shift')
                keyboard.press('right shift')
                pyautogui.press("right",presses=int(keyword[1]),interval=.01)
                keyboard.release('right shift')
                keyboard.release('left shift')

            if keyword[0] == "Key Press":
                if keyword[1] == "TAB":
                    tabInfo = keyword[3]
                    keyboard.wait('tab',suppress=True,trigger_on_release=True)
                    lineNumber,homePressedOnSameLine = moveline(tabInfo[0][1],tabInfo[0][2],lineNumber,homePressedOnSameLine)

                    #highlight
                    keyboard.press('left shift')
                    keyboard.press('right shift')
                    pyautogui.press("right",presses=int(tabInfo[1][1]),interval=.01)
                    keyboard.release('right shift')
                    keyboard.release('left shift')
            
        print(wasNumlockDisabled)
        if wasNumlockDisabled:
                print("turning numlock back on" )
                pyautogui.press('numlock')
        print("end of instructions...")
    
    #helper function for managing moving the cursor around
    def moveline(x,y,lineNumber,homePressedOnSameLine):
        #print(f"X:{x}\nY:{y}\n{lineNumber}")

        if int(y) == lineNumber:
            try:

                if homePressedOnSameLine[lineNumber]:
                    pyautogui.press("right",int(x),interval=.01)
                else:
                    pyautogui.press("right",int(x),interval=.01)
                    pyautogui.press("home")
                    homePressedOnSameLine.insert(lineNumber,True)
            except:
                homePressedOnSameLine.insert(lineNumber,True)
                pyautogui.press("home")
                moveline(x,y,lineNumber,homePressedOnSameLine)
            #print(f"X:{x}\nY:{y}\n{lineNumber}\nHomeBool:{homePressedOnSameLine}")
            return lineNumber, homePressedOnSameLine
        else:
            changeRowNumber = lineNumber - int(y)
            if changeRowNumber > 0:
                pyautogui.press("up",changeRowNumber,interval=.01)
                pyautogui.press("home")
                pyautogui.press("right",int(x),interval=.01)
                lineNumber -=changeRowNumber
                homePressedOnSameLine.insert(lineNumber,True)
                return lineNumber,homePressedOnSameLine
            else:
                changeRowNumber = changeRowNumber * -1
                pyautogui.press("down",changeRowNumber,interval=.01)
                lineNumber += changeRowNumber
                pyautogui.press("home")
                pyautogui.press("right",int(x),interval=.01)
                homePressedOnSameLine.insert(lineNumber,True)
                return lineNumber,homePressedOnSameLine


    #this function is a hot key for the esc key to exit the program
    def my_exit():
        global esc_pressed
        print("Quitting...")
        esc_pressed = True

   
    #initial registaion of our hotkeys and our esc to quit the program
    #the only known limitaion i know of right now is that for some reason adding suppress=True and trigger_on_release=True do not function properly in this area, even though it works up top
    for key in keys:
        keyboard.add_hotkey(key, lambda I = Info[keys.index(key)]: my_function(I))
    

    keyboard.add_hotkey('esc', my_exit)

    try:
        while True:
            keyboard.wait('esc')
            break
    except KeyboardInterrupt:
        pass  
    finally:
        keyboard.unhook_all()

def unpackTrees(trees):
    hotkey = []
    for tree in trees:
        hotkey.append(tree.solve())
    return hotkey








######## MAIN ##############
file = sys.argv[1]
tree = Reader.createCommandTree(file)
HKList = tree.getHKList()

keylist = []
treelist = []
for hotkey in HKList:
    keylist.append(hotkey[0])
    treelist.append(hotkey[1])

keys = formatKeys(keylist) 

info = unpackTrees(treelist)

#starts the main program
HotkeyAction(keys,info)
