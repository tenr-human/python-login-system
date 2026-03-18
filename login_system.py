import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector as con

AdminB = True

# Connect to the database
db_connection = con.connect(host="localhost", user="root", password="your_password", database="login_data")
db_cursor = db_connection.cursor()

# Customize messagebox appearance with updated font and design
def custom_messagebox(title, message, is_error=False):
    custom_root = tk.Toplevel()
    custom_root.title(title)
    custom_root.config(bg="black")  # Black background for message box

    label = tk.Label(custom_root, text=message, font=("Arial", 13, "italic"), fg="white", bg="black")
    label.pack(pady=20, padx=40)

    close_button = tk.Button(custom_root, text="Close", font=("Verdana", 11, "bold"), command=custom_root.destroy)
    close_button.pack(pady=10)

    if is_error:
        label.config(fg="red")  # Keep red color for errors

    custom_root.mainloop()

# Function to handle the login action
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    try:
        db_cursor.execute("SELECT * FROM data WHERE username = %s AND password = %s", (username, password))
        result = db_cursor.fetchall()
        if result:
            custom_messagebox("Login", "Login successful!")
        else:
            custom_messagebox("Login", "Invalid username or password", is_error=True)
    except con.Error as err:
        custom_messagebox("Error", f"An error occurred: {err}", is_error=True)

# Function to handle the registration action
def update_login():
    username = config_username_entry.get().strip()
    password = config_password_entry.get().strip()

    if not username or not password:
        custom_messagebox("Register", "Username and password cannot be empty!", is_error=True)
        return

    try:
        # Check if username already exists
        db_cursor.execute("SELECT * FROM data WHERE username = %s", (username,))
        if db_cursor.fetchone():
            custom_messagebox("Register", "Username already exists!", is_error=True)
            return
        
        # Insert new user into the database
        db_cursor.execute("INSERT INTO data (username, password) VALUES (%s, %s)", (username, password))
        db_connection.commit()

        custom_messagebox("Register", "Registration successful!")
        # After registration, call reset_password to allow the user to change the password
        reset_password(username)

    except con.Error as err:
        custom_messagebox("Error", f"An error occurred: {err}", is_error=True)
    finally:
        config_username_entry.delete(0, tk.END)
        config_password_entry.delete(0, tk.END)


# Function to contact admin
def contact_admin():
    contact_message = simpledialog.askstring("Contact Admin", "Enter your message for the admin(for further details contact:9234567890):", parent=root)
    if contact_message:
        custom_messagebox("Admin Contact", "Message sent to admin:\n" + contact_message)
    else:
        custom_messagebox("Admin Contact", "No message entered", is_error=True)

# Admin Panel Functions
def delete_user():
    username_to_delete = simpledialog.askstring("Delete User", "Enter username to delete:")
    if username_to_delete:
        try:
            db_cursor.execute("DELETE FROM data WHERE username = %s", (username_to_delete,))
            db_connection.commit()
            if db_cursor.rowcount > 0:
                custom_messagebox("Admin", f"User '{username_to_delete}' deleted successfully.")
            else:
                custom_messagebox("Admin", "User not found.", is_error=True)
        except con.Error as err:
            custom_messagebox("Error", f"An error occurred: {err}", is_error=True)

# Function to display the user count and database contents
def display_database():
    try:
        db_cursor.execute("SELECT COUNT(*) FROM data")
        user_count = db_cursor.fetchone()[0]
        db_cursor.execute("SELECT * FROM data")
        users = db_cursor.fetchall()
        message = f"Total number of users: {user_count}\n\n"
        message += "User Database Contents:\n"
        for user in users:
            message += f"Username: {user[0]}, Password: {user[1]}\n"
        custom_messagebox("Admin", message)
    except con.Error as err:
        custom_messagebox("Error", f"An error occurred: {err}", is_error=True)

# Function to create the admin control panel window
def create_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Control Panel")
    admin_window.geometry("400x300")
    admin_window.config(bg="black")

    label = tk.Label(admin_window, text="Admin Control Panel", font=("Courier", 16, 'bold'), fg="white", bg="black")
    label.pack(pady=10)

    admin_button1 = tk.Button(admin_window, text="Delete User", command=delete_user, font=("Arial", 12, 'bold'))
    admin_button1.pack(pady=10)

    admin_button2 = tk.Button(admin_window, text="Display Database", command=display_database, font=("Arial", 12, 'bold'))
    admin_button2.pack(pady=10)

# Function to handle the admin control panel toggle
def admin_control_panel():
    global AdminB
    if AdminB:
        AdminB = False
        authenticate_admin()
        admin_button.config(text="Open Admin Control Panel")
    else:
        AdminB = True
        admin_button.config(text="Close Admin Control Panel")

# Function to authenticate admin
def authenticate_admin():
    admin_username = simpledialog.askstring("Admin Login", "Enter admin username:")
    admin_password = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")
    if admin_username == "admin" and admin_password == "A4DM1N":
        create_admin_panel()
    else:
        custom_messagebox("Admin Login", "Invalid credentials", is_error=True)

def reset_password(username=None):
    if not username:
        username = simpledialog.askstring("Reset Password", "Enter your username:")

    if not username:
        custom_messagebox("Reset Password", "No username entered", is_error=True)
        return

    try:
        db_cursor.execute("SELECT * FROM data WHERE username = %s", (username,))
        result = db_cursor.fetchone()

        if result:
            new_password = simpledialog.askstring("New Password", "Enter your new password:", show="*")
            if not new_password:
                custom_messagebox("Reset Password", "No password entered", is_error=True)
                return

            db_cursor.execute("UPDATE data SET password = %s WHERE username = %s", (new_password, username))
            db_connection.commit()

            custom_messagebox("Reset Password", f"Password reset successful for {username}!")
        else:
            custom_messagebox("Reset Password", "Username not found", is_error=True)
    
    except con.Error as err:
        custom_messagebox("Error", f"An error occurred: {err}", is_error=True)

# Set the window size and make it resizable
root = tk.Tk()
root.title("Login & Configure Page")
root.geometry("1920x1080")
root.config(bg="grey")  # Set background to black

# Frame for the Login Page
login_frame = tk.Frame(root, bg="light grey")
login_frame.pack(pady=20)

login_label = tk.Label(login_frame, text="LOGIN PAGE", font=("Courier", 20, "bold"), fg="white", bg="blue")
login_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Username Label and Entry for Login
login_username_label = tk.Label(login_frame, text="Username:", font=("Arial", 14, "italic"), fg="white", bg="black")
login_username_label.grid(row=1, column=0, sticky="e")
login_username_entry = tk.Entry(login_frame, font=("Arial", 14))
login_username_entry.grid(row=1, column=1, padx=10, pady=5)

# Password Label and Entry for Login
login_password_label = tk.Label(login_frame, text="Password:", font=("Arial", 14, "italic"), fg="white", bg="black")
login_password_label.grid(row=2, column=0, sticky="e")
login_password_entry = tk.Entry(login_frame, font=("Arial", 14), show="*")
login_password_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons for Login
login_button = tk.Button(login_frame, text="Login", font=("Verdana", 14, "bold"), command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

configure_button = tk.Button(login_frame, text="Can't Sign In? Contact Admin", font=("Verdana", 12), command=contact_admin)
configure_button.grid(row=4, column=0, columnspan=2, pady=5)

# Frame for Configure Details
config_frame = tk.Frame(root, bg="light grey")
config_frame.pack(pady=20)

config_label = tk.Label(config_frame, text="CONFIGURE DETAILS", font=("Courier", 20, "bold"), fg="white", bg="blue")
config_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Username Label and Entry for Config
config_username_label = tk.Label(config_frame, text="Username:", font=("Arial", 14, "italic"), fg="white", bg="black")
config_username_label.grid(row=1, column=0, sticky="e")
config_username_entry = tk.Entry(config_frame, font=("Arial", 14))
config_username_entry.grid(row=1, column=1, padx=10, pady=5)

# Password Label and Entry for Config
config_password_label = tk.Label(config_frame, text="Password:", font=("Arial", 14, "italic"), fg="white", bg="black")
config_password_label.grid(row=2, column=0, sticky="e")
config_password_entry = tk.Entry(config_frame, font=("Arial", 14), show="*")
config_password_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons for Configure
config_button1 = tk.Button(config_frame, text="Reset Password", font=("Verdana", 12, "bold"), command=reset_password)
config_button1.grid(row=3, column=0, columnspan=2, pady=5)

config_button2 = tk.Button(config_frame, text="Register", font=("Verdana", 12, "bold"), command=update_login)
config_button2.grid(row=4, column=0, columnspan=2, pady=5)

# Admin control panel button
admin_button = tk.Button(root, text="Admin Control Panel", font=("Verdana", 12, "bold"), command=admin_control_panel)
admin_button.place(relx=0.5, rely=0.8, anchor="center")

root.mainloop()
