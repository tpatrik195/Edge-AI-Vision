import cv2
import requests
import time
import numpy as np
from app.models.segmentation import BackgroundSegmenter
from fastapi import FastAPI, Request
import uvicorn
import threading

SERVER_URL = "http://127.0.0.1:8000"
WEBHOOK_URL = "http://127.0.0.1:9001/webhook"
BACKGROUND_IMG_PATH = "app/pictures/background.jpg"

app = FastAPI()
background_segmenter = BackgroundSegmenter(BACKGROUND_IMG_PATH)

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

def send_frames():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open webcam!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame!")
            break

        _, img_encoded = cv2.imencode('.jpg', frame)
        requests.post(f"{SERVER_URL}/process_frame", files={"frame": img_encoded.tobytes()})

        segmented_frame = background_segmenter.segment_background(frame)

        if segmented_frame is not None:
            cv2.imshow("Received frame with segmentation", segmented_frame)

        if cv2.waitKey(10) == 27:
            print("ESC pressed, unsubscribing...")
            unsubscribe_webhook()
            break

        # time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()

def run_client():
    threading.Thread(target=lambda: uvicorn.run(app, host="127.0.0.1", port=9001), daemon=True).start()
    time.sleep(2)
    subscribe_webhook()
    send_frames()

if __name__ == "__main__":
    run_client()
