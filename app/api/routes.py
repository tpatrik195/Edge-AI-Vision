from fastapi import APIRouter, UploadFile, File
import cv2
import numpy as np
from io import BytesIO
from app.api.process import process_hand_gesture, process_segmentation, process_pose

router = APIRouter()

@router.post("/process_frame")
async def process_frame(frame: UploadFile = File(...)):
    try:
        img_array = np.frombuffer(await frame.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img = cv2.flip(img, 1)
        
        gesture, img = process_hand_gesture(img)
        
        # img = process_segmentation(img)
        # img = process_pose(img)

        cv2.imshow("processed frame", img)
        cv2.waitKey(1)

        return {"message": "frame processed", "gesture": gesture}

    except Exception as e:
        return {"error": str(e)}
