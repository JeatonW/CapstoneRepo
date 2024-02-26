import pyautogui
import pyperclip
import time
from pynput import keyboard

def ex1():
    #if pyautogui.keyDown('ctrl','shift','g'):
        # example for implementing a hotkey containing ctrl shift g
    #pyautogui.hotkey('ctrl','shift','g')

        # sleep to give time for the cursor to go in the right spot
    time.sleep(1)

        # example of a for loop containing range command
    code1 = "for i in range( , ):  \n\tprint(i)\n"

        # put the code onto our clipboard using pyperclip (best i'd find), then paste the code 
        # can also simulate using pyautogui.hotkey('ctrl','v'), but this makes more technical sense with less keypresses
    pyperclip.copy(code1)
    pyautogui.hotkey('ctrl','v')

        # logic for moving the mouse to the position of the first variable
        # WORK IN PROGRESS RN
        #currX,currY = pyautogui.position()
        #print(currX,currY)


    pyautogui.press('up',interval=.01) 
    pyautogui.press('up',interval=.01) 
    i=0
    j=0
    
    # NEED IMPLEMENTATION OF 'TAB' PRESSES
    while i<5:
        pyautogui.press('right',interval=0.01)
        i+= 1
        
    # NEED IMPLEMENTATION OF 'TAB' PRESSES
    # if tab is pressed, we go to next (future implementation)
    while j<11:
         pyautogui.press('right',interval=0.01)
         j+= 1

    # NEED IMPLEMENTATION OF 'TAB' PRESSES
    # if tab is pressed again, we go to the next (future implementation)
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    
    # NEED IMPLEMENTATION OF 'TAB' PRESSES
    # if tab is pressed again, we go to the next section (body of the for loop)
    pyautogui.press('down',interval=.01)
    with pyautogui.hold('shift'):
        with pyautogui.hold('ctrl'):
             pyautogui.press(['left','left'],interval=.01)

    # standard for loop function
    code2 = "\n\nfor i in PLACE:\n\t"

    # code that will copy and paste the code
    pyperclip.copy(code2)
    pyautogui.hotkey('ctrl','v')

    # simulate running through the code
    pyautogui.press('up',interval=.01)
    pyautogui.press('right',interval=.01)
    with pyautogui.hold('shift'):
        pyautogui.press(['left'])
    
    i=0
    while i<5:
        pyautogui.press('right',interval=.01)
        i+=1
    
    # NEED IMPLEMENTATION OF 'TAB' PRESSES
    with pyautogui.hold('shift'):
        with pyautogui.hold('ctrl'):
            pyautogui.press(['right'])
    
    # NEED IMPLEMENTATION OF 'TAB' PRESSES
    # once finished with the variable changes, move down to the body of the for loop
    pyautogui.press('down')

    
    # standard while loop
    code3 = "\n\nwhile :\n\t"
    # code that will copy and paste the code
    pyperclip.copy(code3)
    pyautogui.hotkey('ctrl','v')

    # simulate running through the code
    pyautogui.press('up',interval=.01)
    
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    time.sleep(1)
    
    # if tab is pressed, go to the body of the code
    pyautogui.press('down',interval=.01)

    # standard if statement 
    code4 = "\n\nif FILL:\n\t"

    # code that will copy and paste the code
    pyperclip.copy(code4)
    pyautogui.hotkey('ctrl','v')

    # simulate running the through the code
    pyautogui.press('up',interval=.01)
    pyautogui.press('left',interval=.01)

    # NEED IMPLEMENTATION OF TAB
    with pyautogui.hold('shift'):
        with pyautogui.hold('ctrl'):
            pyautogui.press(['right'])
    time.sleep(1)
    pyautogui.press('down',interval=.01)

    
    # standard if-else statement
    code5 = "\n\nif FILL:\n\t\nelse:\n\t"
    # code to copy and paste the code
    pyperclip.copy(code5)
    pyautogui.hotkey('ctrl','v')

    # simulate running the through the code to print the if-else statement
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('left',interval=.01)
    with pyautogui.hold('shift'):
            pyautogui.press(['right'])

    

    # NEED IMPLEMENTATION OF TAB
    with pyautogui.hold('shift'):
        with pyautogui.hold('ctrl'):
            pyautogui.press(['right'])
    time.sleep(1)

    pyautogui.press('down',interval=.01)
    time.sleep(1)

    pyautogui.press('down',interval=.01)
    pyautogui.press('down',interval=.01)


    # standard if-elif-else statement
    code6 = "\n\nif FILL:\n\t\nelif:\n\t\nelse:\n\t"

    # code to copy and paste the code
    pyperclip.copy(code6)
    pyautogui.hotkey('ctrl','v')

    # simulate running through the code to print out the if-elif-else statement
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('left',interval=.01)
    with pyautogui.hold('shift'):
            with pyautogui.hold('ctrl'):
                 pyautogui.press(['right'])
    time.sleep(1)
    pyautogui.press('down',interval=.01)

    # move to the elif
    time.sleep(1)
    pyautogui.press('down',interval=.01)
    pyautogui.press('down',interval=.01)

    # move to the else
    time.sleep(1)
    pyautogui.press('down',interval=.01)
    pyautogui.press('down',interval=.01)

    # standard break statement contained in a while loop
    code7 = "\n\nwhile :\n\n\tif FILL:\n\t\tbreak\n"
    # code that will copy and paste the code
    pyperclip.copy(code7)
    pyautogui.hotkey('ctrl','v')
    time.sleep(1)

    # simulate running through the code
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('up',interval=.01)
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    pyautogui.press('right',interval=.01)
    time.sleep(1)
    pyautogui.press('down',interval=.01)
    pyautogui.press('down',interval=.01)
    pyautogui.press('right',interval=.01)
    with pyautogui.hold('shift'):
            with pyautogui.hold('ctrl'):
                 pyautogui.press(['right'])

    time.sleep(1)
    pyautogui.press('down',interval=.01)
    pyautogui.press('down',interval=.01)

    

ex1()

