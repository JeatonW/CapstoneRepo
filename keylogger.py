from pynput import keyboard
import time

# class for key listening/logging
class KeyListener:
    # attributes to store state of buggy keys (temp)
    ctrl_pressed = False
    shift_pressed = False

    # initialize the file we will write to
    def __init__(self, commands_file_path="commands.txt"):
        self.commands_file_path = commands_file_path
        self.current_command = ""

    """# placeholder for eventual implementation of commands
    def execute_commands(self,command):
        # ex
        #print(f"Command has been updated: {command}") """

    # def for key listening
    def on_press(self, key):
        try:
            # test keys
            if hasattr(key, 'char'):
                # regular key
                self.current_command += key.char
            # handle spaces separately
            elif key == keyboard.Key.space:
                self.current_command += ' '
            # handle enters as a new command (MUST PRESS TO ADD TO FILE)
            elif key == keyboard.Key.enter:
                with open(self.commands_file_path, 'a') as file:
                    file.write(self.current_command + '\n')
                self.current_command = ""
            else:
                # handle keys such as CTRL as special keys
                key_name = key.name
                if KeyListener.ctrl_pressed:
                    key_name = "CTRL" +key_name
                    KeyListener.ctrl_pressed = False # reset state
                self.current_command += key_name

            # see if the key pressed was esc (ends program)
            if key == keyboard.Key.esc:
                print("Commands have been updated.")
                return False # stop listener

            """# read commands from previosly mentioned file (later implementation)
            with open(self.commands_file_path, 'r') as file:
                commands = file.readlines()"""

            """# exec each command (not implemented)
            for command in commands:
                self.execute_commands(command.strip()) """

        # handle mishaps   
        except Exception as e:
            print(f"Unexpected input: {e}")
    
    
    def start_listener(self):
        # start listening
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

# create instance of KeyListener
listening = KeyListener()
# pause a bit to enable time to swap from the coding window.
time.sleep(3)
# start listening
listening.start_listener()