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

    def draw_hands(self, frame, landmarks, handedness_list):
        if landmarks:
            for hand_landmarks, handedness in zip(landmarks, handedness_list):
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                hand_label = handedness.classification[0].label

                x_min = min([lm.x for lm in hand_landmarks.landmark])
                y_min = min([lm.y for lm in hand_landmarks.landmark])
                x_max = max([lm.x for lm in hand_landmarks.landmark])
                y_max = max([lm.y for lm in hand_landmarks.landmark])

                h, w, _ = frame.shape
                x_min, y_min, x_max, y_max = int(x_min * w), int(y_min * h), int(x_max * w), int(y_max * h)

                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

                cv2.putText(frame, hand_label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    def detect_gesture(self, hand_landmarks, handedness_list):
        if not hand_landmarks or not handedness_list:
            return "none"

        for hand, handedness in zip(hand_landmarks, handedness_list):
            hand_label = handedness.classification[0].label

            landmarks = hand.landmark

            wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
            thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]

            ref_distance = np.sqrt((wrist.x - middle_tip.x) ** 2 + (wrist.y - middle_tip.y) ** 2)

            thumb_index_distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
            index_middle_distance = np.sqrt((index_tip.x - middle_tip.x) ** 2 + (index_tip.y - middle_tip.y) ** 2)
            middle_ring_distance = np.sqrt((middle_tip.x - ring_tip.x) ** 2 + (middle_tip.y - ring_tip.y) ** 2)
            ring_pinky_distance = np.sqrt((ring_tip.x - pinky_tip.x) ** 2 + (ring_tip.y - pinky_tip.y) ** 2)

            norm_thumb_index = thumb_index_distance / ref_distance
            norm_index_middle = index_middle_distance / ref_distance
            norm_middle_ring = middle_ring_distance / ref_distance
            norm_ring_pinky = ring_pinky_distance / ref_distance

            if hand_label == "Right":
                if norm_thumb_index < 0.15 and norm_index_middle < 0.2 and norm_middle_ring < 0.1 and norm_ring_pinky < 0.2:
                    return "-"

                elif norm_thumb_index > 0.5 and norm_index_middle > 0.2 and norm_middle_ring > 0.1 and norm_ring_pinky > 0.3:
                    return "+"
                else:
                    return "normal"
            
        return "none"


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
        # self.bg_segmenter = BackgroundSegmenter("pictures/background.jpg")
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            # frame_segmented = self.bg_segmenter.segment_background(frame)
            frame_segmented = frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            hand_results = self.hand_detector.detect_hands(frame_rgb)
            pose_results = self.pose_detector.detect_pose(frame_rgb)

            handedness_list = hand_results.multi_handedness if hand_results.multi_handedness else []

            self.hand_detector.draw_hands(frame_segmented, hand_results.multi_hand_landmarks, handedness_list)
            self.pose_detector.draw_pose(frame_segmented, pose_results.pose_landmarks)

            gesture = self.hand_detector.detect_gesture(hand_results.multi_hand_landmarks, handedness_list)

            cv2.putText(frame_segmented, f'gesture: {gesture}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('gesture detection', frame_segmented)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = EdgeAiVision()
    app.run()
