#  Laptop Guardian: Unauthorized Access Detection System

This Python-based project uses **face recognition** and **Windows event monitoring** to detect unauthorized login attempts on a laptop. When someone logs in, the system captures an image using your webcam, verifies it against the authorized face, and if unmatched, sends a **Telegram alert** and puts the system to sleep.

---

##  Key Features

-  **Face recognition** using OpenCV & `face_recognition`
-  **Authorized face** registration and encoding
-  **Windows login monitoring** via Security Event Logs (ID 4624/4625)
-  **Intruder image capture**
-  **Telegram alert** with image, timestamp, and location
-  **Auto sleep** the system on detection of an intruder

---

##  File Overview

| File | Description |
|------|-------------|
| `save_authorized_face.py` | Captures and stores the authorized user's face encoding. |
| `laptop_guardian.py` | Continuously monitors login events and performs detection + alert. |
| `authorized_face.pkl` | Binary file storing the encoded face of the authorized user. |
| `intruder/` | Folder where unauthorized access images are stored. |

---

## Setup Instructions

### 1.  Install Dependencies

```bash
pip install opencv-python face_recognition geocoder requests pywin32
```

> Make sure your system has a working webcam and Python 3.8+

---

### 2.  Register Your Authorized Face

Run this script to capture your face and save it for recognition:

```bash
python save_authorized_face.py
```

- Press **`s`** to save when your face is visible.
- The face is stored in a file called `authorized_face.pkl`.

---

### 3.  Start Real-Time Monitoring

Run the main script:

```bash
python laptop_guardian.py
```

It will:
- Monitor Windows Event Logs for login attempts
- Use your webcam to capture the face
- Compare it to the saved authorized face
- If unmatched:
  - Capture image
  - Send Telegram alert
  - Put the laptop to sleep

---

##  Telegram Alerts Setup

1. **Create a Telegram bot** via [@BotFather](https://t.me/BotFather) and get the `BOT_TOKEN`.
2. **Get your `CHAT_ID`**:
   - Message your bot
   - Visit:  
     ```
     https://api.telegram.org/bot<your_bot_token>/getUpdates
     ```
   - Copy the `chat.id` from the response.

3. **Update these in `laptop_guardian.py`:**

```python
BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"
```

---

##  Output Example

When unauthorized access is detected:
- A photo is saved in the `intruder/` folder
- A Telegram alert is sent like:

```
Unauthorized login attempt (Failed) detected!
Time: 2025-07-21 18:00:05
Location: Rajkot, India
[Attached Intruder Photo]
```

---

##  Notes & Limitations

- Works only on **Windows OS** (due to Event Log monitoring via `win32evtlog`)
- Webcam must be enabled and accessible
- Only **one authorized face** is supported at a time
- Accuracy depends on lighting and camera quality
- Ensure `authorized_face.pkl` is in the same folder

---

##  Tested Environment

-  Windows 11
-  Python 3.10
-  Webcam-enabled laptop
-  Telegram Bot API

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
For educational and personal security use only.

---

## Author

**Supriya Kubasad**  
MSc (Cybersecurity & Cyber Law)  
