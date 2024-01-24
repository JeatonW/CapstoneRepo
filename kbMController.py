import pyautogui
import pyperclip
import time
from pynput import keyboard

def ex1():
    #if pyautogui.keyDown('ctrl','shift','g'):
        # example for implementing a hotkey containing ctrl shift g
    pyautogui.hotkey('ctrl','shift','g')

        # sleep to give time for the cursor to go in the right spot
    time.sleep(1)

        # example of a for loop command
    code1 = "for i in range( , ):  \n\tprint(i)\n"

        # put the code onto our clipboard using pyperclip (best i'd find), then paste the code 
        # can also simulate using pyautogui.hotkey('ctrl','v'), but this makes more technical sense with less keypresses
    pyperclip.copy(code1)
    pyautogui.hotkey('ctrl','v')

        # logic for moving the mouse to the position of the first variable
        # WORK IN PROGRESS RN
        #currX,currY = pyautogui.position()
        #print(currX,currY)


    pyautogui.press('up') 
    pyautogui.press('up') 
    i=0
    j=0
    while i<5:
        pyautogui.press('right')
        i+= 1
    #pyautogui.doubleClick()
    # if tab is pressed, we go to next (future implementation)
    while j<11:
         pyautogui.press('right')
         j+= 1

    # if tab is pressed again, we go to the next (future implementation)
    pyautogui.press('right')
    pyautogui.press('right')
    
    # if tab is pressed again, we go to the next section (body of the for loop)
    pyautogui.press('down')
    pyautogui.click()
    with pyautogui.hold('shift'):
        pyautogui.press(['left','left','left','left','left','left','left','left','left'])

ex1()
