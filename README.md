Overview:

This file outlines the structure and functionalities of a python based graphical user interface (GUI) application. It shows the user to sign up and log in using a username and password. User credentials are managed and stored in a JSON file. 


Tools and Libraries Used:

1) tkinter : A standard Python interface to the tk GUI toolkit 
2)json: A module for working with JSON data 
3) os : A module providing a way of using operating system dependent functionality .


File Structure:

USERS_FILE: A JSON file named 'users.json' that stores user data.

load_users(): Function to load user data from the JSON file.

save_users(users): Function to save user data to the JSON file.

login(username, password, users): Function to authenticate users during login.

signup(username, password, users): Function to register new users.

Detailed Description:

1. Importing Modules:
The script starts by importing necessary modules: tkinter, messagebox from tkinter, json, and os.

2. Global Variables:
USERS_FILE is defined as a global variable pointing to 'users.json', which stores user data.

3. Function Definitions:

load_users(): Checks if the user data file exists and loads user data from it.

save_users(users): Accepts a dictionary of user data and saves it to the JSON file.

login(username, password, users): Authenticates a user by checking the provided credentials against stored data.

signup(username, password, users): Registers a new user, ensuring the username does not already exist.
