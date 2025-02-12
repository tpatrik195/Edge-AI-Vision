import cv2
import mediapipe as mp
import numpy as np


class HandGestureDetector:
    def __init__(self, min_detection_conf=0.5, min_tracking_conf=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=min_detection_conf,
                                         min_tracking_confidence=min_tracking_conf)
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hands(self, frame_rgb):
        return self.hands.process(frame_rgb)

    def draw_hands(self, frame, landmarks):
        if landmarks:
            for hand_landmarks in landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def detect_gesture(self, hand_landmarks):
        if not hand_landmarks:
            return "none"

        for hand in hand_landmarks:
            landmarks = hand.landmark

            thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]

            thumb_index_distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
            thumb_pinky_distance = np.sqrt((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2)

            if thumb_index_distance < 0.07 or thumb_pinky_distance < 0.07:
                return "-"

            if thumb_index_distance > 0.3 or thumb_pinky_distance > 0.3:
                return "+"

        return "normal"


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


class BackgroundSegmenter:
    def __init__(self, background_image_path):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
        self.background = cv2.imread(background_image_path)

    def segment_background(self, frame):
        h, w, _ = frame.shape
        self.background = cv2.resize(self.background, (w, h))

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_seg = self.segmentation.process(frame_rgb)
        mask = result_seg.segmentation_mask[:, :, np.newaxis]

        return (frame * mask + self.background * (1 - mask)).astype(np.uint8)


class EdgeAiVision:
    def __init__(self):
        self.hand_detector = HandGestureDetector()
        self.pose_detector = PoseDetector()
        self.bg_segmenter = BackgroundSegmenter("pictures/background.jpg")
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_segmented = self.bg_segmenter.segment_background(frame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            hand_results = self.hand_detector.detect_hands(frame_rgb)
            pose_results = self.pose_detector.detect_pose(frame_rgb)

            self.hand_detector.draw_hands(frame_segmented, hand_results.multi_hand_landmarks)
            self.pose_detector.draw_pose(frame_segmented, pose_results.pose_landmarks)

            gesture = self.hand_detector.detect_gesture(hand_results.multi_hand_landmarks)

            cv2.putText(frame_segmented, f'gesture: {gesture}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('gesture detection', frame_segmented)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = EdgeAiVision()
    app.run()
