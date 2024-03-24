import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os

# Path to the user data file
USERS_FILE = 'users.json'

# Global variables for action history
undo_stack = []
redo_stack = []

# Load users data
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

# Save users data
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
    if password != confirm_password_entry.get():
        messagebox.showerror("Signup Failed", "Passwords do not match.")
        return False
    users[username] = password
    save_users(users)
    messagebox.showinfo("Signup Success", "You have successfully signed up.")
    return True

# Undo action function
def undo_action():
    if not undo_stack:
        messagebox.showinfo("Undo", "No actions to undo.")
        return
    action = undo_stack.pop()
    redo_stack.append(action)  # Prepare for potential redo
    messagebox.showinfo("Undo", "Action undone.")

# Redo action function
def redo_action():
    if not redo_stack:
        messagebox.showinfo("Redo", "No actions to redo.")
        return
    action = redo_stack.pop()
    undo_stack.append(action)  # Allow this action to be undone again
    messagebox.showinfo("Redo", "Action redone.")

# Creating the main window
root = tk.Tk()
root.title("User Authentication System")

# Styling
style = ttk.Style()
style.theme_use('clam')  # Using a more modern theme
bg_color = '#333333'  # Dark background
fg_color = '#ffffff'  # White foreground
button_color = '#0066cc'  # Blue buttons
input_font = font.Font(family="Arial", size=12)
label_font = font.Font(family="Arial", size=14, weight='bold')
root.configure(bg=bg_color)
root.geometry("400x350")  # Adjusted height to accommodate new elements

# Function to switch to login frame
def show_login_frame():
    signup_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Function to switch to signup frame
def show_signup_frame():
    login_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)

# Function to copy text from the focused input field to the clipboard
def copy_text():
    widget = get_focused_input_field()
    if widget:
        try:
            text = widget.selection_get()
            root.clipboard_clear()
            root.clipboard_append(text)
        except tk.TclError:
            messagebox.showwarning('Copy', 'No text selected.')

# Function to cut text from the focused input field to the clipboard
def cut_text():
    widget = get_focused_input_field()
    if widget:
        try:
            copy_text()  # Copy text first
            widget.delete("sel.first", "sel.last")
        except tk.TclError:
            messagebox.showwarning('Cut', 'No text selected.')

# Function to paste text from the clipboard into the focused input field
def paste_text():
    widget = get_focused_input_field()
    if widget:
        try:
            widget.insert(tk.INSERT, root.clipboard_get())
        except tk.TclError:
            messagebox.showwarning('Paste', 'Nothing to paste.')

# Function to show help about creating hotkeys
def show_help():
    help_text = "To create a hotkey:\\n1. Choose a key combination.\\n2. Assign an action to the combination.\\n3. Save your settings."
    messagebox.showinfo("Help - Create Hotkeys", help_text)

# Function to get the currently focused widget
def get_focused_input_field():
    focused_widget = root.focus_get()
    if focused_widget in [username_entry, password_entry, new_username_entry, new_password_entry, confirm_password_entry]:
        return focused_widget
    return None

# Clear Fields functions
def clear_login_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# Clear Fields functions
def clear_login_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def clear_signup_fields():
    new_username_entry.delete(0, tk.END)
    new_password_entry.delete(0, tk.END)
    confirm_password_entry.delete(0, tk.END)

# Update the GUI to include Undo and Redo
def create_menu():
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    file_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Undo", command=undo_action)
    file_menu.add_command(label="Redo", command=redo_action)

    edit_menu = tk.Menu(main_menu, tearoff=0)
    edit_menu.add_command(label="Cut", command=cut_text)
    edit_menu.add_command(label="Copy", command=copy_text)
    edit_menu.add_command(label="Paste", command=paste_text)
    main_menu.add_cascade(label="Edit", menu=edit_menu)

    help_menu = tk.Menu(main_menu, tearoff=0)
    help_menu.add_command(label="How to create hotkeys", command=show_help)
    main_menu.add_cascade(label="Help", menu=help_menu)

create_menu()

# Frames for Login and Signup
login_frame = ttk.Frame(root, padding="10")
signup_frame = ttk.Frame(root, padding="10")

# Login UI Elements
username_label = ttk.Label(login_frame, text="Username:", font=input_font)
username_label.pack(pady=(10, 0))
username_entry = ttk.Entry(login_frame, font=input_font)
username_entry.pack()

password_label = ttk.Label(login_frame, text="Password:", font=input_font)
password_label.pack(pady=(10, 0))
password_entry = ttk.Entry(login_frame, font=input_font, show="*")
password_entry.pack()

remember_me_var = tk.IntVar()
remember_me_check = ttk.Checkbutton(login_frame, text="Remember Me", variable=remember_me_var, onvalue=1, offvalue=0)
remember_me_check.pack(pady=5)

clear_fields_button_login = ttk.Button(login_frame, text="Clear Fields", command=clear_login_fields)
clear_fields_button_login.pack(pady=5)

login_button = ttk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), load_users()))
login_button.pack(pady=10)

to_signup_button = ttk.Button(login_frame, text="Create Account", command=show_signup_frame)
to_signup_button.pack()

# Signup UI Elements
new_username_label = ttk.Label(signup_frame, text="New Username:", font=input_font)
new_username_label.pack(pady=(10, 0))
new_username_entry = ttk.Entry(signup_frame, font=input_font)
new_username_entry.pack()

new_password_label = ttk.Label(signup_frame, text="New Password:", font=input_font)
new_password_label.pack(pady=(10, 0))
new_password_entry = ttk.Entry(signup_frame, font=input_font, show="*")
new_password_entry.pack()

confirm_password_label = ttk.Label(signup_frame, text="Confirm Password:", font=input_font)
confirm_password_label.pack(pady=(5, 0))
confirm_password_entry = ttk.Entry(signup_frame, font=input_font, show="*")
confirm_password_entry.pack()

clear_fields_button_signup = ttk.Button(signup_frame, text="Clear Fields", command=clear_signup_fields)
clear_fields_button_signup.pack(pady=5)

signup_button = ttk.Button(signup_frame, text="Signup", command=lambda: signup(new_username_entry.get(), new_password_entry.get(), load_users()))
signup_button.pack(pady=10)

to_login_button = ttk.Button(signup_frame, text="Already have an account?", command=show_login_frame)
to_login_button.pack()

# Show the login frame initially
show_login_frame()

# Start the application
root.mainloop()


