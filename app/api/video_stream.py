import cv2
import numpy as np
from ..models.pose_detectation import PoseDetector
from ..models.hand_detectation import GestureDetector
from ..models.segmentation import Segmenter

class VideoStreamHandler:
    def __init__(self, video_stream):
        self.video_stream = video_stream
        self.pose_detector = PoseDetector()
        self.gesture_detector = GestureDetector()
        self.segmenter = Segmenter()

    def process_video_stream(self):
        cap = cv2.VideoCapture(self.video_stream)

        ret, frame = cap.read()
        if not ret:
            return None

        frame = self.segmenter.segment(frame)
        frame = self.pose_detector.detect(frame)
        frame = self.gesture_detector.detect(frame)

        _, img_encoded = cv2.imencode('.jpg', frame)
        return img_encoded.tobytes()
