import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self, min_detection_conf=0.5, min_tracking_conf=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=min_detection_conf,
                                      min_tracking_confidence=min_tracking_conf)
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_pose(self, frame_rgb):
        return self.pose.process(frame_rgb)

    def draw_pose(self, frame, landmarks):
        if landmarks:
            self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_pose.POSE_CONNECTIONS)
