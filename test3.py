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
    # Placeholder for undo action logic
    redo_stack.append(action)  # Prepare for potential redo
    messagebox.showinfo("Undo", "Action undone.")

# Redo action function
def redo_action():
    if not redo_stack:
        messagebox.showinfo("Redo", "No actions to redo.")
        return
    action = redo_stack.pop()
    # Placeholder for redo action logic
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
root.geometry("400x300")

# Function to switch to login frame
def show_login_frame():
    signup_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Function to switch to signup frame
def show_signup_frame():
    login_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)

# Update the GUI to include Undo and Redo
def create_menu():
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    
    file_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Undo", command=undo_action)
    file_menu.add_command(label="Redo", command=redo_action)

    help_menu = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="Help", menu=help_menu)
    # Add Help menu items as before

# Initialize UI components
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

login_button = ttk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), load_users()))
login_button.pack(pady=20)

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

signup_button = ttk.Button(signup_frame, text="Signup", command=lambda: signup(new_username_entry.get(), new_password_entry.get(), load_users()))
signup_button.pack(pady=20)

to_login_button = ttk.Button(signup_frame, text="Already have an account?", command=show_login_frame)
to_login_button.pack()

# Show the login frame initially
show_login_frame()

# Start the application
root.mainloop()

