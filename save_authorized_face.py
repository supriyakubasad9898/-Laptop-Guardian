import face_recognition
import cv2
import pickle
import time

print("[*] Starting camera. Please look directly at the camera.")
video = cv2.VideoCapture(0)
time.sleep(2)

saved = False

while True:
    ret, frame = video.read()
    if not ret:
        continue

    # Resize frame to 1/4 size for faster processing (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left) in face_locations:
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.putText(frame, "Press 's' to save your face", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow("Capture Authorized Face", frame)

    key = cv2.waitKey(1)
    if key == ord('s') and face_encodings:
        # Only use the first face encoding
        authorized_face = face_encodings[0]
        with open("authorized_face.pkl", "wb") as f:
            pickle.dump(authorized_face, f)
        print("[+] Face encoding saved as 'authorized_face.pkl'")
        saved = True
        break
    elif key == 27:  # ESC to exit
        break

video.release()
cv2.destroyAllWindows()

if not saved:
    print("[!] No face saved. Try again by rerunning the script.")
