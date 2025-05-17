import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess

# Set initial admin password
admin_password = "admin123"

def check_password():
    entered_password = password_entry.get()
    global admin_password
    
    if entered_password == admin_password:
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        root.destroy()
        subprocess.run(["python", "gui.py"])  # Open gui.py
    else:
        messagebox.showerror("Login Failed", "Wrong code! Please try again.")
        password_entry.delete(0, tk.END)  # Clear the entry field

def change_password():
    global admin_password
    new_password = simpledialog.askstring("Change code", "Enter new admin password:", show='*')
    if new_password:
        admin_password = new_password
        messagebox.showinfo("Success", "Admin code changed successfully!")

# Create main window
root = tk.Tk()
root.title("Admin Login")
root.geometry("1600x900")

# Create Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Change Password", command=change_password)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

bg_image = Image.open("C:/Users/DELL/Desktop/Python/BG Img/f_bg.png")
bg_image = bg_image.convert("RGBA")  # Convert to RGBA format to support transparency
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
alpha = 170  # Set desired opacity level here (128 is 50% transparent)
bg_image.putalpha(alpha)
p = ImageTk.PhotoImage(bg_image)
b = tk.Label(root, image=p)
b.place(x=0, y=0, relwidth=1, relheight=1)  

# Label
label = tk.Label(root, text="Enter Admin Code",font=("Helvetica",20,"bold"),bg="black",fg="white")
label.place(x=550,y=114)

# Password Entry
password_entry = tk.Entry(root, show="*",font=("Helvetica",20,"bold"))
password_entry.place(x=520,y=214)

# Login Button
login_button = tk.Button(root, text="Login", command=check_password,font=("Helvetica",20,"bold"),bg="red",fg="white")
login_button.place(x=620,y=280)

# Run the GUI
root.mainloop()
