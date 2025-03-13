from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
import cv2
import numpy as np
import requests
from app.api.process import process_hand_gesture, process_segmentation, process_pose

router = APIRouter()

subscribers = set()

latest_segmented_frame = None

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
    global latest_segmented_frame
    try:
        img_array = np.frombuffer(await frame.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img = cv2.flip(img, 1)

        gesture, img = process_hand_gesture(img)

        segmented_img = process_segmentation(img)
        latest_segmented_frame = segmented_img

        await notify_subscribers(gesture)

        # cv2.imshow("processed frame", img)
        # cv2.waitKey(1)

        return {"message": "frame processed"}

    except Exception as e:
        return {"error": str(e)}

@router.get("/next_frame")
async def next_frame():
    global latest_segmented_frame

    if latest_segmented_frame is None:
        raise HTTPException(status_code=404, detail="No frame available")

    success, img_encoded = cv2.imencode('.jpg', latest_segmented_frame)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode frame")

    return Response(content=img_encoded.tobytes(), media_type="image/jpeg")
