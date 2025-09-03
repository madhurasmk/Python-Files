import tkinter as tk
import webbrowser
from tkinter import messagebox, END

def login():
    """Handles the login logic."""
    username = username_entry.get()
    password = password_entry.get()

    # **Replace with your actual authentication logic**
    # This is a placeholder for demonstration purposes.
    if username == "admin" and password == "pwd":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")  # Success message
    elif username == "user" and password == "12345":
        messagebox.showinfo("Login Successful", "Welcome, User!")  # Success message
        webbrowser.open("Index.html")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")  # Error message


def clear():
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    resp = messagebox.askyesno("Confirmation", "Do u want to continue?")
    if resp:
        username_entry.focus_set()
    else:
        root.destroy()


# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("500x200")  # Set window size

# Username Label and Entry
# username_label = tk.Label(root, text="Username:")
# username_label.pack(pady=(10))  # Add vertical padding
#
# username_entry = tk.Entry(root)
# username_entry.pack()
#
# # Password Label and Entry
# password_label = tk.Label(root, text="Password:")
# password_label.pack(pady=(15))
#
# password_entry = tk.Entry(root, show="*")  # Hide password characters
# password_entry.pack()
#
# # Login Button
# clear_button = tk.Button(root, text="Clear", command=clear)
# clear_button.pack(pady=(60))
#
# # Login Button
# login_button = tk.Button(root, text="Login", command=login)
# login_button.pack(pady=(0, 80))


tk.Label(root, text="Username:").grid(row=20, column=50, padx=2, pady=2)
username_entry = tk.Entry(root)
username_entry.grid(row=20, column=70, padx=20, pady=20)
#
tk.Label(root, text="Password:").grid(row=40, column=50, padx=5, pady=5)
password_entry =tk.Entry(root)
password_entry.grid(row=40, column=70, padx=20, pady=20)

# Create Buttons
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=60, column=60, padx=15, pady=5)
clear_button = tk.Button(root, text="Clear", command=clear)
clear_button.grid(row=60, column=65, padx=15, pady=5)
# Keep the window open
root.mainloop()

# # PyQt6 demo
# from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
# import  sys
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Hello World")
#         button = QPushButton("My Simple App")
#         button.pressed.connect(self.close)
#         self.setCentralWidget(button)
#         self.show()
#
# app = QApplication(sys.argv)
# w = MainWindow()
# app.exec()
