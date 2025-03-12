from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np
import requests
from app.api.process import process_hand_gesture, process_segmentation, process_pose

router = APIRouter()

subscribers = set()

@router.post("/subscribe_webhook")
async def subscribe_webhook(url: str):
    if url in subscribers:
        raise HTTPException(status_code=400, detail="Already subscribed")
    subscribers.add(url)
    return {"message": f"Subscribed: {url}"}

@router.post("/unsubscribe_webhook")
async def unsubscribe_webhook(url: str):
    if url not in subscribers:
        raise HTTPException(status_code=400, detail="Not subscribed")
    subscribers.remove(url)
    return {"message": f"Unsubscribed: {url}"}

async def notify_subscribers(gesture):
    for url in list(subscribers):
        try:
            requests.post(url, json={"gesture": gesture})
        except Exception as e:
            print(f"Failed to notify {url}: {e}")

@router.post("/process_frame")
async def process_frame(frame: UploadFile = File(...)):
    try:
        img_array = np.frombuffer(await frame.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img = cv2.flip(img, 1)

        gesture, img = process_hand_gesture(img)

        await notify_subscribers(gesture)

        # cv2.imshow("processed frame", img)
        # cv2.waitKey(1)

        return {"message": "frame processed"}

    except Exception as e:
        return {"error": str(e)}
