import tkinter as tk
from tkinter import messagebox, Menu
from database import *
from camera import take_photo
from security import validate_access_code, update_access_code  # Ensure update_access_code is correctly imported
from notifications import send_sms
import re
import datetime
from tkinter import PhotoImage, Label
from PIL import Image, ImageTk
import sqlite3
from tkinter import ttk

class SocietySecuritySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Society Security System")
        self.create_main_interface()

    def create_main_interface(self):
        self.root.geometry("1600x900")
        bg_image = Image.open("C:/Users/DELL/Desktop/Python/BG Img/f_bg.png")
        bg_image = bg_image.convert("RGBA")  # Convert to RGBA format to support transparency
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)


        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 170  # Set desired opacity level here (128 is 50% transparent)
        bg_image.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p = ImageTk.PhotoImage(bg_image)

        # Display the image on a label as the backound
        self.b = tk.Label(self.root, image=self.p)
        self.b.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch image to fit window

        self.new_guest_btn = tk.Button(self.root, text="New Guest", font=("Helvetica",10,"bold"),bg="gray",fg="white",command=self.new_guest, height=2,width=20,relief="solid")
        self.new_guest_btn.place(x=240, y=214)  # Adjust position as needed

        self.new_member_btn = tk.Button(self.root, text="New Society Member",font=("Helvetica",10,"bold"),bg="gray",fg="white",command=self.new_member,height=2,width=20,relief="solid")
        self.new_member_btn.place(x=600, y=214)  # Adjust position as needed

        self.already_visit_btn = tk.Button(self.root, text="Already Visit",font=("Helvetica",10,"bold"),bg="gray",fg="white", command=self.already_visit,height=2,width=20,relief="solid")
        self.already_visit_btn.place(x=950, y=214)  # Adjust position as needed

        self.view_data_btn = tk.Button(self.root, text="View Data",font=("Helvetica",10,"bold"),bg="gray",fg="white", command=self.view_data,height=2,width=20,relief="solid")
        self.view_data_btn.place(x=420, y=356)  # Adjust position as needed

        self.manipulate_btn = tk.Button(self.root, text="Manipulate", font=("Helvetica",10,"bold"),bg="gray",fg="white",command=self.manipulate_data,height=2,width=20,relief="solid")
        self.manipulate_btn.place(x=775, y=356)  # Adjust position as needed

        # Add menu for notices, alerts, and access code change
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.society_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Society Menu", menu=self.society_menu)

        self.society_menu.add_command(label="Society Notice", command=self.write_notice)
        self.society_menu.add_command(label="Fire Alert", command=self.send_fire_alert)
        self.society_menu.add_command(label="Emergency Alert", command=self.send_emergency_alert)
        self.society_menu.add_command(label="Change Access Code", command=self.change_access_code)
        self.society_menu.add_command(label="Find Guest Data", command=self.find_guest_data)

    # Placeholder methods for button commands
    def new_guest(self): pass
    def new_member(self): pass
    def already_visit(self): pass
    def view_data(self): pass
    def manipulate_data(self): pass
    def write_notice(self): pass
    def send_fire_alert(self): pass
    def send_emergency_alert(self): pass
    def change_access_code(self): pass
    def find_guest_data(self): pass
    
    def validate_phone(self, phone):
        return re.match(r"^[1-9]\d{9}$", phone) is not None

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
    
    def new_guest(self):
        guest_window = tk.Toplevel(self.root)

        bg_image2 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/Guest_bg.png")
        bg_image2 = bg_image2.convert("RGBA")
        bg_image2 = bg_image2.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        alpha = 180
        bg_image2.putalpha(alpha)
        self.p2 = ImageTk.PhotoImage(bg_image2)

        self.b2 = tk.Label(guest_window, image=self.p2)
        self.b2.place(x=0, y=0, relwidth=1, relheight=1)

        guest_window.title("New Guest Registration")
        guest_window.geometry("1600x900")

        tk.Label(guest_window, text="Enter the Guest Information", font=("", 25, "bold"), fg="red").place(x=450, y=40)
        tk.Label(guest_window, text="Guest Full Name", font=(20)).place(x=500, y=120)
        name_entry = tk.Entry(guest_window, font=(20))
        name_entry.place(x=650, y=120)

        tk.Label(guest_window, text="Phone Number", font=(20)).place(x=500, y=170)
        phone_entry = tk.Entry(guest_window, font=(20))
        phone_entry.place(x=650, y=170)

        tk.Label(guest_window, text="Visit Flat Number", font=(20)).place(x=500, y=220)
        flat_entry = tk.Entry(guest_window, font=(20))
        flat_entry.place(x=650, y=220)

        tk.Label(guest_window, text="Reason for Visit", font=(20)).place(x=500, y=270)
        reason_entry = tk.Entry(guest_window, font=(20))
        reason_entry.place(x=650, y=270)

        tk.Label(guest_window, text="Vehicle Number", font=(20)).place(x=500, y=320)
        vehicle_entry = tk.Entry(guest_window, font=(20))
        vehicle_entry.place(x=650, y=320)

        def validate_vehicle_number(vehicle_number):
            return vehicle_number.isalnum() and len(vehicle_number) in [10, 1]
        def submit_guest():
            name = name_entry.get()
            phone = phone_entry.get()
            flat = flat_entry.get()
            reason = reason_entry.get()
            vehicle_number = vehicle_entry.get()
            visit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            guest = get_guest(name)
            if guest:
                messagebox.showinfo("Visited", f"This Guest has already visited, allow to entry")
                return
            if not all([name, phone, flat, reason, vehicle_number]):
                messagebox.showerror("Warning", "Fill the complete information")
                return

            if not phone.isdigit() or len(phone) != 10:
                messagebox.showerror("Invalid Phone", "Please enter a valid phone number.")
                return

            if not validate_vehicle_number(vehicle_number):
                messagebox.showerror("Invalid Vehicle Number", "Vehicle number must be alphanumeric with a length of 10 or 1.")
                return

            if not validate_flat(flat):
                messagebox.showerror("Invalid Flat Number", "This flat number is not registered in the society.")
                return

            # Assume take_photo() and insert_guest() are defined elsewhere
            photo_path = take_photo(f"C:/Users/DELL/Desktop/Python/Photos/{name}.jpg")
            insert_guest(name, phone, flat, visit_time, reason, vehicle_number, photo_path)

            messagebox.showinfo("Success", "Guest registered successfully!")
            send_sms(phone, f"Guest {name} is visiting flat {flat}.")

        tk.Button(guest_window, text="Submit", command=submit_guest, font=(20)).place(x=650, y=380)
        tk.Button(
            guest_window, 
            text="Back", 
            command=guest_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=566, y=380)
    
    def new_member(self):
        member_window = tk.Toplevel(self.root)
        bg_image3 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/acs_c.png")
        bg_image3 = bg_image3.convert("RGBA")  # Convert to RGBA format to support transparency

        bg_image3 = bg_image3.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 140  # Set desired opacity level here (128 is 50% transparent)
        bg_image3.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p2 = ImageTk.PhotoImage(bg_image3)

        # Display the image on a label as the backound
        self.b2 = tk.Label(member_window, image=self.p2)
        self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
        member_window.title("New Society Member Registration")
        member_window.geometry("1600x900")
        tk.Label(member_window, text="Enter Access Code",font=("",20,"bold"),fg="green").place(x=564,y=170)
        code_entry = tk.Entry(member_window, show="*",font=(40))
        code_entry.place(x=600,y=220)

        def verify_code():
            access_code = code_entry.get()
            if validate_access_code(access_code):
                self.register_member(member_window)
            else:
                messagebox.showerror("Error", "Invalid Access Code")

        tk.Button(member_window, text="Submit", command=verify_code,font=(30)).place(x=700,y=270)
        tk.Button(
            member_window, 
            text="Back", 
            command= member_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=620, y=270)

    def register_member(self, member_window):
        member_windows = tk.Toplevel(self.root)
        bg_image4 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/Guest_bg.png")
        bg_image4 = bg_image4.convert("RGBA")  # Convert to RGBA format to support transparency

        bg_image4 = bg_image4.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 180  # Set desired opacity level here (128 is 50% transparent)
        bg_image4.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p2 = ImageTk.PhotoImage(bg_image4)

        # Display the image on a label as the backound
        self.b2 = tk.Label(member_windows, image=self.p2)
        self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
        member_windows.title("New Society Member Registration")
        member_windows.geometry("1600x900")
        member_windows.title("Register Society Member")
        tk.Label(member_windows,text="Enter the Society Member Info",font=("",25,"bold"),fg="red").place(x=440,y=40)
        
        tk.Label(member_windows, text="Member Name",font=(20)).place(x=500,y=120)
        name_entry = tk.Entry(member_windows,font=(20))
        name_entry.place(x=650,y=120)

        tk.Label(member_windows, text="Flat Number",font=(20)).place(x=500,y=170)
        flat_entry = tk.Entry(member_windows,font=(20))
        flat_entry.place(x=650,y=170)

        tk.Label(member_windows, text="Phone Number",font=(20)).place(x=500,y=220)
        phone_entry = tk.Entry(member_windows,font=(20))
        phone_entry.place(x=650,y=220)

        tk.Label(member_windows, text="Email",font=(20)).place(x=500,y=270)
        email_entry = tk.Entry(member_windows,font=(20))
        email_entry.place(x=650,y=270)

        tk.Label(member_windows, text="Rented or Own",font=(20)).place(x=500,y=320)
        status_entry = tk.Entry(member_windows,font=(20))
        status_entry.place(x=650,y=320)

        def submit_member():
            name = name_entry.get()
            phone = phone_entry.get()
            flat = flat_entry.get()
            email = email_entry.get()
            status = status_entry.get()

            if name == "" or flat == "" or status == "":
                messagebox.showerror("Warning", "Fill the complete information")
            elif not self.validate_phone(phone):
                messagebox.showerror("Invalid Phone", "Please enter a valid phone number.")
                return
            elif not self.validate_email(email):
                messagebox.showerror("Invalid Email", "Please enter a valid email ID.")
                return
            elif status!="Rented" and status!="rented" and status!="Own" and status!="own":
                messagebox.showerror("Invalid Status", "Please enter a valid status.")
                return
            else:
                conflict = check_member_existence(phone, email, flat, name)
                if conflict == "phone":
                    messagebox.showerror("Duplicate Phone", "This phone number is already registered.")
                elif conflict == "email":
                    messagebox.showerror("Duplicate Email", "This email ID is already registered.")
                elif conflict == "flat":
                    messagebox.showerror("Duplicate Flat", "This flat number is already registered.")
                elif conflict == "name":
                    messagebox.showerror("Duplicate Name", "A member with this name already exists.")
                elif conflict == "member":
                    messagebox.showerror("Duplicate Member", "This member already exists.")
                else:
                    insert_member(name, phone, flat, email, status)
                    messagebox.showinfo("Success", "Society member registered successfully!")
                    member_windows.destroy()
        tk.Button(member_windows, text="Submit", command=submit_member,font=(30)).place(x=650,y=380)
        tk.Button(
            member_windows, 
            text="Back", 
            command=member_windows.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=560, y=380)

    def already_visit(self):
        visit_window = tk.Toplevel(self.root)
        bg_image5 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/GExist.png")
        bg_image5 = bg_image5.convert("RGBA")  # Convert to RGBA format to support transparency
        bg_image5 = bg_image5.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 140  # Set desired opacity level here (128 is 50% transparent)
        bg_image5.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p2 = ImageTk.PhotoImage(bg_image5)

        # Display the image on a label as the background
        self.b2 = tk.Label(visit_window, image=self.p2)
        self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
        visit_window.title("Already Visit Check")
        visit_window.geometry("1600x900")

        # Input field for Guest Name
        tk.Label(visit_window, text="Guest Full Name", font=("", 15, "bold"), bg="gray", fg="white").place(x=613, y=170)
        name_entry = tk.Entry(visit_window, font=(20))
        name_entry.place(x=600, y=220)
        
        # Function to check guest details
        def check_guest():
            name = name_entry.get()
            guest = get_guest(name)
            if guest:
                messagebox.showinfo("Success", f"Welcome back, {guest[1]}! Entry allowed.")
            else:
                messagebox.showerror("Error", "No entry, please register as a new guest first.")
        
        # "Check" Button
        tk.Button(visit_window, text="Check", command=check_guest, font=(20), bg="gray", fg="white").place(x=700, y=270)
        
        # "Back" Button
        tk.Button(
            visit_window, 
            text="Back", 
            command=visit_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
        ).place(x=620, y=270)

    
    def view_data(self):
        view_window = tk.Toplevel(self.root)
        bg_image6 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/show_d.png")
        bg_image6 = bg_image6.convert("RGBA")  # Convert to RGBA format to support transparency

        bg_image6 = bg_image6.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 100  # Set desired opacity level here (128 is 50% transparent)
        bg_image6.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p2 = ImageTk.PhotoImage(bg_image6)

        # Display the image on a label as the backound
        self.b2 = tk.Label(view_window, image=self.p2)
        self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
        view_window.title("View Data")
        view_window.geometry("1600x900")
        tk.Button(
            view_window, 
            text="Back", 
            command=view_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=660, y=330)
        def view_guests():
            view_window2 = tk.Toplevel(self.root)
            bg_image7 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/show_d.png").convert("RGBA")
            bg_image7 = bg_image7.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            bg_image7.putalpha(100)
            self.p2 = ImageTk.PhotoImage(bg_image7)
            self.b2 = tk.Label(view_window2, image=self.p2)
            self.b2.place(x=0, y=0, relwidth=1, relheight=1)

            view_window2.title("All Data")
            view_window2.geometry("1600x900")

            # Columns for Treeview
            columns = ("Sr. No.", "Name", "Phone", "Flat", "Visit Time", "Reason", "Vehicle")
            tree = ttk.Treeview(view_window2, columns=columns, show="headings")
            tree.pack(side="left", fill="both", expand=True, padx=20, pady=20)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120 if col == "Sr. No." else 150, anchor="center")

            guests = get_all_guests()
            if guests:
                for i, guest in enumerate(guests, start=1):
                    tree.insert("", "end", values=(i, guest[1], guest[2], guest[3], guest[4], guest[5], guest[7]))
            else:
                tk.Label(view_window2, text="No data available.", font=("", 14, "bold"), fg="white", bg="gray").pack(pady=20)

            scrollbar = ttk.Scrollbar(view_window2, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="left", fill="y")

            # Image display frame
            image_label = tk.Label(view_window2, bg="white", borderwidth=2, relief="solid")
            image_label.place(x=1150, y=200, width=300, height=300)

            # Guest info display
            info_label = tk.Label(view_window2, text="", font=("Arial", 12, "bold"), bg="white", fg="black", justify="left", anchor="nw")
            info_label.place(x=1150, y=520, width=300, height=150)

            # Row selection handler
            def on_row_selected(event):
                selected_item = tree.focus()
                if not selected_item:
                    return
                values = tree.item(selected_item)['values']
                name = values[1]
                phone = values[2]
                flat = values[3]
                visit_time = values[4]
                reason = values[5]
                vehicle = values[6]

                # Load guest image by phone number
                image_path = f"C:/Users/DELL/Desktop/Python/Guest_Images/{phone}.jpg"
                try:
                    img = Image.open(image_path)
                    img = img.resize((300, 300), Image.LANCZOS)
                    guest_img = ImageTk.PhotoImage(img)
                    image_label.config(image=guest_img, text="")
                    image_label.image = guest_img  # prevent garbage collection
                except Exception as e:
                    image_label.config(image="", text="Image not found", bg="white")
                    print(f"Image load error: {e}")

                # Show guest details
                info_text = f"Name: {name}\nPhone: {phone}\nFlat: {flat}\nVisit Time: {visit_time}\nReason: {reason}\nVehicle: {vehicle}"
                info_label.config(text=info_text)

            tree.bind("<<TreeviewSelect>>", on_row_selected)


        def view_members():
            view_window3 = tk.Toplevel(self.root)
            bg_image8 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/show_d.png")
            bg_image8 = bg_image8.convert("RGBA")
            bg_image8 = bg_image8.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

            alpha = 100  
            bg_image8.putalpha(alpha)
            self.p2 = ImageTk.PhotoImage(bg_image8)

            self.b2 = tk.Label(view_window3, image=self.p2)
            self.b2.place(x=0, y=0, relwidth=1, relheight=1)

            view_window3.title("All Society Members")
            view_window3.geometry("1600x900")

            # Updated columns with Sr. No.
            columns = ("Sr. No.", "Name", "Flat", "Phone", "E-mail", "Status")
            tree = ttk.Treeview(view_window3, columns=columns, show="headings")
            tree.pack(fill="both", expand=True, padx=20, pady=20)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120 if col == "Sr. No." else 200, anchor="center")

            members = get_all_members()

            if members:
                for i, member in enumerate(members, start=1):
                    tree.insert("", "end", values=(i, member[1], member[3], member[2], member[4], member[5]))
            else:
                tk.Label(view_window3, text="No data available.", font=("", 14, "bold"), fg="white", bg="gray").pack(pady=20)

            scrollbar = ttk.Scrollbar(view_window3, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

        tk.Label(view_window, text=f"Which Data you want show ?",font=("",20,"bold"),fg="red",bg="black").place(x=500,y=120)
        tk.Button(view_window, text="View Guest Data", command=view_guests,font=("",15),bg="Gray",fg="white").place(x=450,y=220)
        tk.Button(view_window, text="View Society Member Data", command=view_members,font=("",15),fg="white",bg="gray").place(x=700,y=220)

    def write_notice(self):
        notice_window = tk.Toplevel(self.root)
        notice_window.title("Write Society Notice")
        
        tk.Label(notice_window, text="Enter Notice").pack()
        notice_text = tk.Text(notice_window, height=10, width=40)
        notice_text.pack()

        def send_notice():
            notice = notice_text.get("1.0", "end").strip()
            members = get_all_members()
            for member in members:
                send_sms(member[2], f"Society Notice: {notice}")
            messagebox.showinfo("Success", "Notice sent to all members.")
            notice_window.destroy()

        tk.Button(notice_window, text="Send Notice", command=send_notice).pack()

    def send_fire_alert(self):
        members = get_all_members()
        for member in members:
            send_sms(member[2], "Emergency: Fire Alert! Please evacuate the building.")
        messagebox.showinfo("Alert Sent", "Fire alert sent to all members.")

    def send_emergency_alert(self):
        members = get_all_members()
        for member in members:
            send_sms(member[2], "Emergency: Immediate attention required! Please follow safety protocols.")
        messagebox.showinfo("Alert Sent", "Emergency alert sent to all members.")

    def change_access_code(self):
        code_window = tk.Toplevel(self.root)
        code_window.title("Change Access Code")
        
        tk.Label(code_window, text="Enter New Access Code").pack()
        new_code_entry = tk.Entry(code_window, show="*")
        new_code_entry.pack()

        def save_code():
            new_code = new_code_entry.get()
            update_access_code(new_code)  # Ensure the update_access_code function is implemented
            messagebox.showinfo("Success", "Access code updated successfully!")
            code_window.destroy()

        tk.Button(code_window, text="Submit", command=save_code).pack()

    def find_guest_data(self):
        # Create a new window for the inputs
        find_window = tk.Toplevel(self.root)
        find_window.title("Find Guest Data")
        find_window.geometry("1600x900")
        bg_image10 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/find_bg.png")
        bg_image10 = bg_image10.convert("RGBA")  # Convert to RGBA format to support transparency
        bg_image10 = bg_image10.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 135  # Set desired opacity level here (128 is 50% transparent)
        bg_image10.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p = ImageTk.PhotoImage(bg_image10)

        # Display the image on a label as the backound
        self.b = tk.Label(find_window, image=self.p)
        self.b.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch image to fit window

        tk.Label(find_window, text=f"Find Specific Guest",font=("",20,"bold"),fg="red",bg="black").place(x=563,y=40)

        # Input fields
        tk.Label(find_window, text="Date (YYYY-MM-DD):",font=("",10,"bold")).place(x=624, y=110)
        date_entry = tk.Entry(find_window,font=("",10,""))
        date_entry.place(x=620, y=140)

        tk.Label(find_window, text="From Time (HH:MM:SS):",font=("",10,"bold")).place(x=620, y=190)
        from_time_entry = tk.Entry(find_window,font=("",10,""))
        from_time_entry.place(x=620, y=220)

        tk.Label(find_window, text="To Time (HH:MM:SS):",font=("",10,"bold")).place(x=624, y=270)
        to_time_entry = tk.Entry(find_window,font=("",10,""))
        to_time_entry.place(x=620, y=300)

        def show_results_in_new_window(data):
            # Create a new window for displaying results
            results_window = tk.Toplevel(self.root)
            results_window.title("Guest Data Results")
            results_window.geometry("1600x900")

            # Create a Treeview for tabular display
            columns = ("ID", "Name", "Phone", "Flat", "Visit Time", "Reason", "Vehicle")
            tree = ttk.Treeview(results_window, columns=columns, show="headings")
            tree.pack(fill="both", expand=True, padx=10, pady=10)

            # Define column headings
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")

            # Populate the tree with data
            if data:
                for row in data:
                    tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("No Data", "No guests found for the given date and time range.")

        def search_guests():
            date = date_entry.get()
            from_time = from_time_entry.get()
            to_time = to_time_entry.get()

            try:
                # Fetch data from the database
                guest_data = get_guest_data(date, from_time, to_time)
                show_results_in_new_window(guest_data)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Search button
        search_button = tk.Button(find_window, text="Search", command=search_guests,font=("",13,""))
        search_button.place(x=698, y=340)
        tk.Button(
            find_window, 
            text="Back", 
            command=find_window.destroy,  # Close the current window and return to the previous one
            font=(13), 
            bg="red", 
            fg="white"
            ).place(x=620, y=340)
        
    def manipulate_data(self):
        manipulate_window = tk.Toplevel(self.root)
        bg_image9 = Image.open("C:/Users/DELL/Desktop/Python/BG Img/manipu_d.png")
        bg_image9 = bg_image9.convert("RGBA")  # Convert to RGBA format to support transparency

        bg_image9 = bg_image9.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

        # Adjust opacity (0 is fully transparent, 255 is fully opaque)
        alpha = 140  # Set desired opacity level here (128 is 50% transparent)
        bg_image9.putalpha(alpha)

        # Convert to a Tkinter-compatible image
        self.p2 = ImageTk.PhotoImage(bg_image9)

        # Display the image on a label as the backound
        self.b2 = tk.Label(manipulate_window, image=self.p2)
        self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
       
        manipulate_window.title("Manipulate Data")
        manipulate_window.geometry("1600x900")
        
        
        def delete_guest():
            guest_window = tk.Toplevel(manipulate_window)
            bg_imag = Image.open("C:/Users/DELL/Desktop/Python/BG Img/manipu_d.png")
            bg_imag = bg_imag.convert("RGBA")  # Convert to RGBA format to support transparency

            bg_imag = bg_imag.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

            # Adjust opacity (0 is fully transparent, 255 is fully opaque)
            alpha = 140  # Set desired opacity level here (128 is 50% transparent)
            bg_imag.putalpha(alpha)

            # Convert to a Tkinter-compatible image
            self.p2 = ImageTk.PhotoImage(bg_imag)

            # Display the image on a label as the backound
            self.b2 = tk.Label(guest_window, image=self.p2)
            self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
            guest_window.geometry("1600x900")
            guest_window.title("Delete Guest")
            tk.Label(guest_window, text="Enter Guest Name",font=(20)).place(x=620,y=170)
            guest_name_entry = tk.Entry(guest_window,font=(20))
            guest_name_entry.place(x=600,y=220)
            
            def delete_guest_data():
                name = guest_name_entry.get()  # Get the name from the Entry widget

                # Connect to the database
                conn = sqlite3.connect('society.db')  # Replace 'society.db' with your database name
                cursor = conn.cursor()

                # Check if the member exists in the database
                cursor.execute("SELECT * FROM guests WHERE name=?", (name,))
                record = cursor.fetchone()

                if record:
                    # Member found, proceed with deletion
                    cursor.execute("DELETE FROM guests WHERE name=?", (name,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Guest '{name}' has been deleted.")
                else:
                    # Member not found, show an error message
                    messagebox.showwarning("Error", f"Guest '{name}' not found.")

                # Close the database connection
                conn.close()
            tk.Button(guest_window, text="Delete", command=delete_guest_data,font=(30)).place(x=700,y=270)
            tk.Button(
            guest_window, 
            text="Back", 
            command=guest_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=620, y=270)

        def delete_member():
            member_window = tk.Toplevel(manipulate_window)
            bg_ima = Image.open("C:/Users/DELL/Desktop/Python/BG Img/manipu_d.png")
            bg_ima = bg_ima.convert("RGBA")  # Convert to RGBA format to support transparency

            bg_ima = bg_ima.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)

            # Adjust opacity (0 is fully transparent, 255 is fully opaque)
            alpha = 140  # Set desired opacity level here (128 is 50% transparent)
            bg_ima.putalpha(alpha)

            # Convert to a Tkinter-compatible image
            self.p2 = ImageTk.PhotoImage(bg_ima)

            # Display the image on a label as the backound
            self.b2 = tk.Label(member_window, image=self.p2)
            self.b2.place(x=0, y=0, relwidth=1, relheight=1) 
            member_window.geometry("1600x900")
            member_window.title("Delete Member")

            tk.Label(member_window, text="Enter Member Name",font=(20)).place(x=620,y=170)
            member_name_entry = tk.Entry(member_window,font=(20))
            member_name_entry.place(x=600,y=220)

            def delete_member_data():
                name = member_name_entry.get()  # Get the name from the Entry widget

                # Connect to the database
                conn = sqlite3.connect('society.db')  # Replace 'society.db' with your database name
                cursor = conn.cursor()

                # Check if the member exists in the database
                cursor.execute("SELECT * FROM members WHERE name=?", (name,))
                record = cursor.fetchone()

                if record:
                    # Member found, proceed with deletion
                    cursor.execute("DELETE FROM members WHERE name=?", (name,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Member '{name}' has been deleted.")
                else:
                    # Member not found, show an error message
                    messagebox.showwarning("Error", f"Member '{name}' not found.")

                # Close the database connection
                conn.close()

            tk.Button(member_window, text="Delete", command=delete_member_data,font=(30)).place(x=700,y=270)
            tk.Button(
            member_window, 
            text="Back", 
            command=member_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=620, y=270)

        tk.Label(manipulate_window, text=f"Who's Data you want Delete ?",font=("",20,"bold"),fg="red").place(x=500,y=120)
        tk.Button(manipulate_window, text="Guest", command=delete_guest,font=("",15)).place(x=590,y=220)
        tk.Button(manipulate_window, text="Member", command=delete_member,font=("",15)).place(x=690,y=220)
        tk.Button(
            manipulate_window, 
            text="Back", 
            command=manipulate_window.destroy,  # Close the current window and return to the previous one
            font=(20), 
            bg="red", 
            fg="white"
            ).place(x=660, y=290)

root = tk.Tk()
create_tables()
app = SocietySecuritySystem(root)
root.mainloop()
