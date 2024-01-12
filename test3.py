
import tkinter as tk
from tkinter import messagebox
import json
import os

# Path to the user data file
USERS_FILE = 'users.json'

# Function to load users data
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

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

class IDEHotkeysApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IDE Hotkeys Customizer")
        self.geometry("800x600")
        self.users = load_users()
        self.create_menu()  # Create the menu bar with the Help option
        self.create_login_signup_frame()
        self.i = 0

    def create_login_signup_frame(self):
        self.login_signup_frame = tk.Frame(self)
        self.login_signup_frame.pack(pady=50)

        self.username_label = tk.Label(self.login_signup_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_signup_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_signup_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_signup_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_signup_frame, text="Login", command=self.perform_login)
        self.login_button.grid(row=2, column=0)

        #add a theme change button
        self.theme_option_button = tk.Button(self.login_signup_frame,text = "Darkmode", command=self.perform_theme_change)
        self.theme_option_button.grid(row=2,column=1)

        self.signup_button = tk.Button(self.login_signup_frame, text="Signup", command=self.perform_signup)
        self.signup_button.grid(row=2, column=2)

    #function to perform appropriate color changes on everything in the window
    def perform_theme_change(self):

        #default for the window is white so this section changes every bg to black and fg to white
        if self.i == 0:
            
            #changes background of whole window
            self.configure(bg="#1c241e")
            
            #changes the theme text and fg and bg colors
            self.theme_option_button.configure(text="lightmode",fg="white",bg="#1c241e")
            #udpates i
            self.i = 1

            #changes color of login frame
            self.login_signup_frame.configure(bg="#1c241e")
            self.login_button.configure(fg="white",bg="#1c241e")
            self.signup_button.configure(fg="white",bg="#1c241e")
            self.password_label.configure(fg="white",bg="#1c241e")
            self.username_label.configure(fg="white",bg="#1c241e")
            #self.help_menu.configure(fg="white",bg="#1c241e")




        else:
            #changes menues back to white
            self.configure(bg="white")
            self.theme_option_button.configure(text="Darkmode",fg="#1c241e",bg="white")
            self.login_signup_frame.configure(bg="white")
            self.login_button.configure(fg="#1c241e",bg="white")
            self.signup_button.configure(fg="#1c241e",bg="white")
            self.password_label.configure(fg="#1c241e",bg="white")
            self.username_label.configure(fg="#1c241e",bg="white")
            








            self.i = 0

    def perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login(username, password, self.users):
            self.login_signup_frame.destroy()
            self.create_main_frame()

    def perform_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if signup(username, password, self.users):
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def create_main_frame(self):
        if self.i == 1:
            bg = "#1c241e"
            fg = "white"
        else:
            bg = "white"
            fg = "#1c241e"

        self.main_frame = tk.Frame(self,bg=bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
     
        
        load_script_button = tk.Button(self.main_frame, text="Load Script", command=self.load_script,bg=bg,fg=fg)
        load_script_button.pack(pady=(10, 0))

        create_new_script_button = tk.Button(self.main_frame, text="Create New Script", command=self.create_new_script,bg=bg,fg=fg)
        create_new_script_button.pack(pady=(10, 0))

        manage_ides_button = tk.Button(self.main_frame, text="Manage IDEs", command=self.manage_ides,bg=bg,fg=fg)
        manage_ides_button.pack(pady=(10, 0))

    def load_script(self):
        # Placeholder for loading script functionality
        pass

    def create_new_script(self):
        # Placeholder for creating new script functionality
        pass

    def manage_ides(self):
        # Placeholder for managing IDEs functionality
        pass

    # Create the help menu and its functionalities
    def create_menu(self):
        menu_bar = tk.Menu(self)
        
        #menu_bar.configure(bg="#1c241e")
        
        self.config(menu=menu_bar)
        
       
        #can add colors to help_menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Create Hotkeys", command=self.show_hotkey_help)

    def show_hotkey_help(self):
        help_message = "To create a hotkey:\n1. Go to the 'Create New Script' section.\n2. Enter the name of the IDE and the hotkey combination you wish to use.\n3. Describe the action the hotkey will perform.\n4. Click 'Save' to store your new hotkey."
        messagebox.showinfo("How to Create Hotkeys", help_message)

def main():
    app = IDEHotkeysApp()
    app.mainloop()

if __name__ == "__main__":
    main()
