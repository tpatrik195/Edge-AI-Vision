import cv2
import requests
import time

SERVER_URL = "http://127.0.0.1:8000/process_frame"

def send_frame():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("error: cannot open webcam!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("error: cannot read frame!")
            break

        _, img_encoded = cv2.imencode('.jpg', frame)

        response = requests.post(SERVER_URL, files={"frame": img_encoded.tobytes()})

        print(f"server response: {response.text}")

        time.sleep(0.1)

    cap.release()

if __name__ == "__main__":
    send_frame()
