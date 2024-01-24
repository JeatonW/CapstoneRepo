
import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os

# Path to the user data file
USERS_FILE = 'users.json'

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

# Frames for Login and Signup
login_frame = ttk.Frame(root)
signup_frame = ttk.Frame(root)

# Function to switch to login frame
def show_login_frame():
    signup_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Function to switch to signup frame
def show_signup_frame():
    login_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)

# Login UI Elements
login_label = ttk.Label(login_frame, text="Login", font=label_font)
login_label.pack(pady=10)

username_label = ttk.Label(login_frame, text="Username", font=input_font)
username_label.pack()
username_entry = ttk.Entry(login_frame, font=input_font)
username_entry.pack()

password_label = ttk.Label(login_frame, text="Password", font=input_font)
password_label.pack()
password_entry = ttk.Entry(login_frame, font=input_font, show="*")
password_entry.pack()

login_button = ttk.Button(login_frame, text="Login", style='Accent.TButton', command=lambda: login(username_entry.get(), password_entry.get(), load_users()))
login_button.pack(pady=10)

to_signup_button = ttk.Button(login_frame, text="Create Account", command=show_signup_frame)
to_signup_button.pack()

# Signup UI Elements
signup_label = ttk.Label(signup_frame, text="Signup", font=label_font)
signup_label.pack(pady=10)

new_username_label = ttk.Label(signup_frame, text="Username", font=input_font)
new_username_label.pack()
new_username_entry = ttk.Entry(signup_frame, font=input_font)
new_username_entry.pack()

new_password_label = ttk.Label(signup_frame, text="Password", font=input_font)
new_password_label.pack()
new_password_entry = ttk.Entry(signup_frame, font=input_font, show="*")
new_password_entry.pack()

signup_button = ttk.Button(signup_frame, text="Signup", style='Accent.TButton', command=lambda: signup(new_username_entry.get(), new_password_entry.get(), load_users()))
signup_button.pack(pady=10)

to_login_button = ttk.Button(signup_frame, text="Already have an account?", command=show_login_frame)
to_login_button.pack()

# Initialize with login frame
show_login_frame()

# Start the application
root.mainloop()
