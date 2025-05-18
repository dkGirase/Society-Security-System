# 🏡 Society Security System

The **Society Security System** is a desktop application developed in **Python** using **Tkinter**. It helps manage the entry and security data for a residential society, including **guest registration**, **member registration**, **photo capture**, **alert notifications**, and more.

---

## 🔧 Features

- 🧾 **Guest Registration**
  - Add guest details with validations
  - Capture and store guest photo
  - Check-in/Check-out management

- 👥 **Society Member Registration**
  - Register society members with contact details
  - Photo capture and storage

- 📸 **Photo Integration**
  - Captures image via webcam and saves to database/directory

- 📊 **View Guest and Member Records**
  - Treeview-based display with filter/search options
  - View stored images

- ⚠️ **Emergency Alerts**
  - Fire, Theft, and Emergency SMS alerts to members

- 📩 **Society Notices**
  - Admin can write and send notices to all members

- 🔐 **Access Code Management**
  - Change security access code with authentication

- 📱 **SMS Notification System**
  - Sends SMS alerts for check-in, emergency, and notice updates (using Twilio or other services)

- 🖼️ **Custom Background UI**
  - Background image with opacity and custom soft fonts for clean design

---

## 💻 Technologies Used

- **Python 3.10+**
- **Tkinter** – GUI Library
- **PIL (Pillow)** – Image processing
- **SQLite3 / MySQL** – Database
- **OpenCV** – Webcam image capture
- **Twilio API** – SMS notifications (optional)
- **ttk Treeview** – Tabular data display

---

## 📁 Folder Structure

SocietySecuritySystem/
├── assets/
│ ├── backgrounds/
│ └── photos/
├── db/
│ └── society.db
├── src/
│ ├── main.py
│ ├── guest_registration.py
│ ├── member_registration.py
│ ├── alerts.py
│ ├── notice.py
│ └── utils/
│ ├── validation.py
│ ├── image_handler.py
│ └── sms_sender.py
├── README.md
└── requirements.txt


---

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/society-security-system.git
   cd society-security-system

2.Install dependencies:
   pip install -r requirements.txt

3.Run the main application:
  python src/main.py

🔒 Security & Validation
Email and phone validation during registration

Access code verification before sensitive actions

Logs entry and exit timestamps

👨‍💻 Author
Dnyanendra Girase
TY BBA-CA (B2)
Society Security System Project – 2025
