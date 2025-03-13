import cv2
import requests
import time
import numpy as np
from fastapi import FastAPI, Request
import uvicorn
import threading

SERVER_URL = "http://127.0.0.1:8000"
WEBHOOK_URL = "http://127.0.0.1:9001/webhook"
BACKGROUND_IMG_PATH = "app/pictures/background.jpg"

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(f"Gesture Event Received: {data}")
    return {"status": "received"}

def subscribe_webhook():
    response = requests.post(f"{SERVER_URL}/subscribe_webhook", params={"url": WEBHOOK_URL})
    print(f"Subscription Response: {response.text}")

def unsubscribe_webhook():
    response = requests.post(f"{SERVER_URL}/unsubscribe_webhook", params={"url": WEBHOOK_URL})
    print(f"Unsubscription Response: {response.text}")

def get_next_frame():
    try:
        response = requests.get(f"{SERVER_URL}/next_frame")
        if response.status_code == 200:
            img_array = np.frombuffer(response.content, np.uint8)
            segmented_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return segmented_img
        else:
            print(f"Error getting next frame: {response.text}")
            return None
    except Exception as e:
        print(f"Failed to get next frame: {e}")
        return None

def send_frames():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open webcam!")
        return

    background = cv2.imread(BACKGROUND_IMG_PATH)
    if background is None:
        print(f"Error: Cannot load background image from {BACKGROUND_IMG_PATH}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame!")
            break

        frame = cv2.resize(frame, (320, 240))
        _, img_encoded = cv2.imencode('.jpg', frame)
        requests.post(f"{SERVER_URL}/process_frame", files={"frame": img_encoded.tobytes()})

        segmented_img = get_next_frame()
        if segmented_img is not None:
            segmented_img = cv2.resize(segmented_img, (background.shape[1], background.shape[0]))

            mask = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)
            mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)[1]

            result = background.copy()
            result[mask > 0] = segmented_img[mask > 0]

            cv2.imshow("Received frame from api with segmentation", result)

        if cv2.waitKey(10) == 27:
            print("ESC pressed, unsubscribing...")
            unsubscribe_webhook()
            break

        time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()

def run_client():
    threading.Thread(target=lambda: uvicorn.run(app, host="127.0.0.1", port=9001), daemon=True).start()
    time.sleep(2)
    subscribe_webhook()
    send_frames()

if __name__ == "__main__":
    run_client()
