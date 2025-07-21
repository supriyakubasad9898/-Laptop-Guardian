import os
import sys
import pickle
import cv2
import face_recognition
import datetime
import requests
import geocoder
import win32evtlog
import time

# === Telegram Configuration ===
BOT_TOKEN = "7760352760:AAGiO0TpkcsISm4Imk5JwIBgRT3Y500uDT8"
CHAT_ID = "790397947"

def send_telegram_alert(img_path, message):
    try:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
        location = geocoder.ip('me')
        files = {'photo': open(img_path, 'rb')}
        data = {
            'chat_id': CHAT_ID,
            'caption': f"{message}\nTime: {datetime.datetime.now()}\nLocation: {location.city}, {location.country}"
        }
        requests.post(url, files=files, data=data)
    except Exception as e:
        print(f"[!] Telegram alert failed: {e}")

def load_authorized_face():
    try:
        with open("authorized_face.pkl", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print("[!] Authorized face encoding not found.")
        sys.exit(1)

def detect_face(authorized_encoding):
    video = cv2.VideoCapture(0)
    ret, frame = video.read()
    video.release()
    if not ret:
        return None, False
    face_locations = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, face_locations)
    for encoding in encodings:
        match = face_recognition.compare_faces([authorized_encoding], encoding, tolerance=0.5)
        if match[0]:
            return frame, True
    return frame, False

def monitor_events(authorized_encoding):
    server = 'localhost'
    logtype = 'Security'
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    processed_events = set()

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            time.sleep(3)
            continue

        for event in events:
            if event.EventID in [4624, 4625]:  # Success or Failed login
                record_id = event.RecordNumber
                if record_id in processed_events:
                    continue
                processed_events.add(record_id)

                frame, is_authorized = detect_face(authorized_encoding)
                if not is_authorized:
                    status = "Success" if event.EventID == 4624 else "Failed"
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    # Create 'intruder' folder if not exists
                    intruder_folder = os.path.join(os.getcwd(), "intruder")
                    os.makedirs(intruder_folder, exist_ok=True)

                    # Save image in that folder
                    img_path = os.path.join(intruder_folder, f"intruder_{timestamp}_{record_id}.jpg")

                    if frame is not None:
                        cv2.imwrite(img_path, frame)
                        send_telegram_alert(img_path, f"🚨 Unauthorized login attempt ({status}) detected!")

                    print("[!] Unauthorized user detected. Sleeping in 5 seconds...")
                    time.sleep(5)
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        time.sleep(3)

if __name__ == "__main__":
    authorized_encoding = load_authorized_face()
    monitor_events(authorized_encoding)
