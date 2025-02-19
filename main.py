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
            index_mcp = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_mcp = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_mcp = landmarks[self.mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
            pinky_mcp = landmarks[self.mp_hands.HandLandmark.PINKY_MCP]

            def calculate_angle(p1, p2, point):
                vector_1 = np.array([p1.x - point.x, p1.y - point.y])
                vector_2 = np.array([p2.x - point.x, p2.y - point.y])

                dot_product = np.dot(vector_1, vector_2)
                magnitude_1 = np.linalg.norm(vector_1)
                magnitude_2 = np.linalg.norm(vector_2)

                if magnitude_1 == 0 or magnitude_2 == 0:
                    return 0

                cos_theta = dot_product / (magnitude_1 * magnitude_2)
                angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
                return np.degrees(angle_rad)

            thumb_index_angle = calculate_angle(thumb_tip, index_tip, wrist)
            index_middle_angle = calculate_angle(index_tip, middle_tip, wrist)
            middle_ring_angle = calculate_angle(middle_tip, ring_tip, wrist)
            ring_pinky_angle = calculate_angle(ring_tip, pinky_tip, wrist)

            wrist_index_angle = calculate_angle(wrist, index_tip, index_mcp)
            wrist_middle_angle = calculate_angle(wrist, middle_tip, middle_mcp)
            wrist_ring_angle = calculate_angle(wrist, ring_tip, ring_mcp)
            wrist_pinky_angle = calculate_angle(wrist, pinky_tip, pinky_mcp)

            # print(f"thumb - index angle: {thumb_index_angle}\nindex - middle angle: {index_middle_angle}\nmiddle - ring angle: {middle_ring_angle}\nring - pinky angle: {ring_pinky_angle}\n")
            # print(f"wrist - index angle: {wrist_index_angle}\nwrist - middle angle: {wrist_middle_angle}\nwrist - ring angle: {wrist_ring_angle}\nwrist - pinky angle: {wrist_pinky_angle}\n")

            if hand_label == "Right":
                if thumb_index_angle < 2 and index_middle_angle < 4 and middle_ring_angle < 5 and ring_pinky_angle < 2:
                    return "-"

                elif thumb_index_angle > 30 and index_middle_angle > 5 and middle_ring_angle > 5 and ring_pinky_angle > 10:
                    return "+"

                elif wrist_index_angle > 160 and wrist_middle_angle < 25 and wrist_ring_angle < 20 and wrist_pinky_angle < 20:
                    return "pointing"

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
        # self.pose_detector = PoseDetector()
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
            # pose_results = self.pose_detector.detect_pose(frame_rgb)

            handedness_list = hand_results.multi_handedness if hand_results.multi_handedness else []

            self.hand_detector.draw_hands(frame_segmented, hand_results.multi_hand_landmarks, handedness_list)
            # self.pose_detector.draw_pose(frame_segmented, pose_results.pose_landmarks)

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
