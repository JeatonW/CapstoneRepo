
import tkinter as tk
from tkinter import messagebox
import json
import os
import reader

# Path to the user data file
USERS_FILE = 'users.json'
CONFIG_FILE = 'config.json'

# Function to load users data
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

#used read from the config.json
def load_settings():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

#called when the save button is clicked
def save_config(settings):
    with open(CONFIG_FILE,'w') as file:
        json.dump(settings, file)

# Function to save users data
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

# Login function
def login(username, password, users):
    if username in users and users[username] == password:
        messagebox.showinfo("Login Success", "You have successfully logged in.")
        return True
    messagebox.showerror("Login Failed", "Incorrect username or password.")
    return False

# Signup function
def signup(username, password, users):
    if username in users:
        messagebox.showerror("Signup Failed", "Username already exists.")
        return False
    users[username] = password
    save_users(users)
    messagebox.showinfo("Signup Success", "You have successfully signed up.")
    return True




#main tkinter window start
class IDEHotkeysApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("IDE Hotkeys Customizer")
        self.geometry("800x600")
        self.users = load_users()
        self.settings = load_settings()
        #self.create_menu()  # Create the menu bar with the Help option
        self.bg = self.settings["bg"]
        self.file = "pseudolang_test.txt"
        self.create_login_signup_frame()

        

    def create_login_signup_frame(self):
        self.login_signup_frame = tk.Frame(self,bg=self.bg)
        self.login_signup_frame.pack(fill=tk.BOTH,expand = True)

        #self.username_label = tk.Label(self.login_signup_frame, text="Username:",bg=self.bg)
        #self.username_label.grid(row=1, column=1)

        self.username_entry = tk.Entry(self.login_signup_frame)
        self.username_entry.grid(row=1, column=1,ipadx = 20,sticky = "w")
        self.username_entry.insert(0,"Username")
        self.username_entry.bind("<FocusIn>",self.clear_username)

        #self.password_label = tk.Label(self.login_signup_frame, text="Password:",bg=self.bg)
        #self.password_label.grid(row=2, column=1)

        self.password_entry = tk.Entry(self.login_signup_frame)
        self.password_entry.grid(row=2, column=1,ipadx = 20,pady = (0,5),sticky = "w")
        self.password_entry.insert(0,"Password")
        self.password_entry.bind("<FocusIn>",self.clear_password)

        self.login_button = tk.Button(self.login_signup_frame, text="Login", command=self.perform_login)
        self.login_button.grid(row=4, column=1,ipadx=60,pady = (10,0),sticky = "w")

        self.signup_button = tk.Button(self.login_signup_frame, text="Signup", command=self.perform_signup)
        self.signup_button.grid(row=5, column=1,ipadx=56,sticky = "w")
        
        self.login_signup_frame.grid_columnconfigure((0,2), weight=1)
        self.login_signup_frame.grid_rowconfigure((0,6,7,8,9),weight=1)


    def clear_username(self,e):
         self.username_entry.delete(0,"end")
    def clear_password(self,e):
        self.password_entry.delete(0,"end")
    #function to perform appropriate color changes on everything in the window
    
    #called when the login button is pressed
    def perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login(username, password, self.users):
            self.login_signup_frame.destroy()
            self.create_main_frame()
            self.create_menu()

    #called when the signup button is pressed
    def perform_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if signup(username, password, self.users):
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    #creates the starting frame and its buttons
    def create_main_frame(self):

        self.main_frame = tk.Frame(self,bg=self.bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
     
        
        load_script_button = tk.Button(self.main_frame, text="Load Script", command=self.load_script)
        load_script_button.pack(pady=(10, 0))

        create_new_script_button = tk.Button(self.main_frame, text="Create New Script", command=self.create_new_script)
        create_new_script_button.pack(pady=(10, 0))

        manage_ides_button = tk.Button(self.main_frame, text="Manage IDEs", command=self.manage_ides)
        manage_ides_button.pack(pady=(10, 0))

    def load_script(self):
        tree = Reader.createCommandTree(self.file)
        tree.solveAndPrint()
        # Placeholder for loading script functionality

        #will have each hotkeys keys displayed need window
        mini_window = tk.Tk()
        mini_window.title("Keys")
        mini_window.geometry("250x150")
        key_list = []

        #organizes file into a nested list
        with open(self.file) as x:
            for line in x:
                if line[0] != "\t" and line[0].isalpha() and line[0] != "\n":
                    key_list.append(line.replace("\n","").replace(" ","").replace(":","").split("+"))
                else:
                    pass
        #creates the frame in the window and loops through the key_list to display the buttons in window
        key_background = tk.Frame(mini_window,bg = self.bg)
        key_background.pack(fill=tk.BOTH,expand = True)
        sep = " + "
        
        #creates labesl and buttons for how ever many hotkeys there are
        for i in key_list:
            x = key_list.index(i)
            name = tk.Label(key_background,text = f"Key Number:{x}")
            name.grid(row=x,column=1)
            key = tk.Button(key_background,text = sep.join(i))
            key.grid(row=x,column=2,sticky='',padx=5) 
        
        #adds weight to the edge grids to center it
        key_background.grid_columnconfigure((0,3), weight=1)
        mini_window.mainloop()
    
    def create_new_script(self):
        # Placeholder for creating new script functionality
        pass

    def manage_ides(self):
        # Placeholder for managing IDEs functionality
        pass



    #called when the settings button in the menu bar is clicked
    def go_to_settings(self):
        self.main_frame.destroy()
        self.create_settings()


    #Create the help menu and its functionalities
    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        #creates the help tab in the menu bar
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Create Hotkeys", command=self.show_hotkey_help)

        #createst a setting tab
        settings_menu = tk.Menu(menu_bar,tearoff=0)
        menu_bar.add_cascade(label="Settings",menu=settings_menu)
        settings_menu.add_command(label="Change Settings",command=self.go_to_settings)

    #displays a message after help menu button is clicked
    def show_hotkey_help(self):
        help_message = "To create a hotkey:\n1. Go to the 'Create New Script' section.\n2. Enter the name of the IDE and the hotkey combination you wish to use.\n3. Describe the action the hotkey will perform.\n4. Click 'Save' to store your new hotkey."
        messagebox.showinfo("How to Create Hotkeys", help_message)

    #saves the settings
    def save(self,variable):
        self.update()
        #manually set catigory need to find a way to grab the box name
        catigory = "bg"
        print(variable.get())
        value = variable.get()
        self.configure_json(catigory,value,self.settings)
        
        #this needs to a function that recalls everything in the config
        self.bg = self.settings["bg"]

        #need a smarter way to update the current window, might just have to configure this manaully tho
        self.settings_display.config(bg=self.bg)
        self.update()
    def configure_json(self,catigory,value, settings):
            settings[catigory] = value
            save_config(settings)
    #reposible for creating the entire settings frame/window
    def create_settings(self):
        self.update()

        #background of the settings window
        self.settings_window = tk.Frame(self,bg=self.bg,width=self.winfo_width())
        self.settings_window.pack(fill = tk.BOTH,side = tk.TOP,anchor = tk.NE,expand = True)

        #settings frame on the left that holds the buttons
        self.settings_frame = tk.Frame(self.settings_window, bg = self.bg,width=20,height = self.winfo_height())
        self.settings_frame.pack(side=tk.LEFT,anchor = tk.W,fill=tk.Y)

        #window the the right of the button that displays the currently selected section/button
        self.settings_display = tk.Frame(self.settings_window,bg = self.bg)
        self.settings_display.pack(side=tk.RIGHT,anchor=tk.E,expand = True,fill=tk.BOTH,pady=5)


        #everything under here is under the settings_display frame and should inherit from such

        #note when adding stuff to here Grid should be used as it is easier to allight stuff

        Colors = ["red","orange","yellow","green","blue","purple","pink","brown","gray","white","black"]
        variable = tk.StringVar(self.settings_display)
        variable.set(Colors[9]) #default value of the list

        variable2 =tk.StringVar(self.settings_display)
        variable2.set(Colors[9])

        bg_label = tk.Label(self.settings_display,text="Background Color:")
        bg_option = tk.OptionMenu(self.settings_display,variable,*Colors)

        fg_label = tk.Label(self.settings_display,text="Forground Color:")        
        fg_option = tk.OptionMenu(self.settings_display,variable2,*Colors)

        bg_label.grid(row=0,column=1,sticky='') 
        bg_option.grid(row=0,column=2,sticky='')
        
        fg_label.grid(row=1,column=1,sticky='')
        fg_option.grid(row=1,column=2,sticky='')
        

        save_button = tk.Button(self.settings_display,text="Save",command=lambda: self.save(variable))
        save_button.grid(row=2,column=2,sticky='')
        self.settings_display.grid_columnconfigure((0,3), weight=1)

        ########################end of settings display######################


        #all buttons on the left hand side of the settings menue will go here
        profile = tk.Button(self.settings_frame,text="profile",fg="black",font=5)
        profile.pack(side= tk.TOP,anchor = tk.W,fill=tk.BOTH,expand=True)

        preferences_settings = tk.Button(self.settings_frame,text="Preferences",fg="black",font=5)
        preferences_settings.pack(side= tk.TOP,anchor = tk.N,fill=tk.BOTH,expand=True)

        other_settings = tk.Button(self.settings_frame,text="other",fg="black",font=5)
        other_settings.pack(side= tk.TOP,anchor = tk.N,fill=tk.BOTH,expand=True)

        placeholder = tk.Button(self.settings_frame,text="rdm",fg="black",font=5)
        placeholder.pack(side= tk.TOP,anchor = tk.N,fill=tk.BOTH,expand=True)

        #theback button destroys the settings window and rebuilds the main frame and menu bar
        back = tk.Button(self.settings_frame,text="back",command=lambda:[self.settings_window.destroy(),self.create_main_frame(),self.create_menu()],fg="black",font=10)
        back.pack(side= tk.TOP,anchor = tk.N,fill=tk.BOTH,expand=True)

    






def main():
    app = IDEHotkeysApp()
    app.mainloop()

if __name__ == "__main__":
    main()
    #atexit.register()
