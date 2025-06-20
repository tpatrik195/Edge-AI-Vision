import cv2
import mediapipe as mp
import numpy as np

class HandGestureDetector:
    def __init__(self, min_detection_conf=0.5, min_tracking_conf=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=min_detection_conf,
                                         min_tracking_confidence=min_tracking_conf)
        self.mp_drawing = mp.solutions.drawing_utils
        self.prev_left_orientation = None
        self.prevprev_left_orientation = None  

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
    
    def get_index_tip_position(self, hand_landmarks, image_shape):
        if not hand_landmarks:
            return None

        landmark = hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        h, w, _ = image_shape
        x_px = int(landmark.x * w)
        y_px = int(landmark.y * h)
        return x_px, y_px

    def detect_gesture(self, hand_landmarks, handedness_list, frame):
        if not hand_landmarks or not handedness_list:
            return "None"

        left_fist = False
        right_fist = False
        left_open = False
        right_open = False
        hand_gesture = "None"
        left_orientation = "unknown"
        right_orientation = "unknown"

        for hand, handedness in zip(hand_landmarks, handedness_list):
            hand_label = handedness.classification[0].label
            landmarks = hand.landmark

            wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
            thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
            thumb_mcp = landmarks[self.mp_hands.HandLandmark.THUMB_MCP]
            index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mcp = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_mcp = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_mcp = landmarks[self.mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
            pinky_mcp = landmarks[self.mp_hands.HandLandmark.PINKY_MCP]

            def is_hand_upward(landmarks):
                x0 = landmarks[self.mp_hands.HandLandmark.WRIST].x
                y0 = landmarks[self.mp_hands.HandLandmark.WRIST].y
                x9 = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                y9 = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                dx = x9 - x0
                dy = y9 - y0
                if abs(dx) < 1e-5:
                    dx = 1e-5
                slope = dy / dx
                return abs(slope) > 1 and y9 < y0
            
            def is_hand_leftward(landmarks):
                x0 = landmarks[self.mp_hands.HandLandmark.WRIST].x
                y0 = landmarks[self.mp_hands.HandLandmark.WRIST].y
                x9 = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                y9 = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                dx = x9 - x0
                dy = y9 - y0
                if dx == 0:
                    return False
                m = dy / dx
                if 0 < abs(m) < 1 and x9 < x0:
                    return True
                else:
                    return False
            
            def is_hand_rightward(landmarks):
                x0 = landmarks[self.mp_hands.HandLandmark.WRIST].x
                y0 = landmarks[self.mp_hands.HandLandmark.WRIST].y
                x9 = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                y9 = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                dx = x9 - x0
                dy = y9 - y0
                if dx == 0:
                    return False
                m = dy / dx
                if 0 < abs(m) < 1 and x9 > x0:
                    return True
                else:
                    return False
            
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
            
            def is_palm_facing(landmarks):
                thumb_x = landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x
                pinky_x = landmarks[self.mp_hands.HandLandmark.PINKY_TIP].x
                if thumb_x < pinky_x:
                    return True
                else:
                    return False
                
            def is_left_fist(landmarks, mp_hands):
                thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
                if not (thumb_tip.x < thumb_mcp.x):
                    return False
                finger_tip_ids = [
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP,
                ]
                finger_mcp_ids = [
                    mp_hands.HandLandmark.INDEX_FINGER_MCP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                    mp_hands.HandLandmark.RING_FINGER_MCP,
                    mp_hands.HandLandmark.PINKY_MCP,
                ]
                for tip_id, mcp_id in zip(finger_tip_ids, finger_mcp_ids):
                    tip = landmarks[tip_id]
                    mcp = landmarks[mcp_id]
                    if not (tip.y > mcp.y):
                        return False
                return True

            def is_right_fist(landmarks, mp_hands):
                thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
                thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
                if not (thumb_tip.x > thumb_mcp.x):
                    return False
                finger_tip_ids = [
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP,
                ]
                finger_mcp_ids = [
                    mp_hands.HandLandmark.INDEX_FINGER_MCP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                    mp_hands.HandLandmark.RING_FINGER_MCP,
                    mp_hands.HandLandmark.PINKY_MCP,
                ]
                for tip_id, mcp_id in zip(finger_tip_ids, finger_mcp_ids):
                    tip = landmarks[tip_id]
                    mcp = landmarks[mcp_id]
                    if not (tip.y > mcp.y):
                        return False
                return True
            
            def is_flat_open_hand(landmarks, mp_hands, threshold=0.04):
                extended = True
                for finger in ["INDEX_FINGER", "MIDDLE_FINGER", "RING_FINGER", "PINKY"]:
                    tip = landmarks[getattr(mp_hands.HandLandmark, f"{finger}_TIP")]
                    pip = landmarks[getattr(mp_hands.HandLandmark, f"{finger}_PIP")]
                    if not (tip.y < pip.y):
                        extended = False
                        break
                if not extended:
                    return False
                index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].x
                pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].x
                distances = [
                    abs(index_tip - middle_tip),
                    abs(middle_tip - ring_tip),
                    abs(ring_tip - pinky_tip),
                ]
                if any(d > threshold for d in distances):
                    return False
                return True

            thumb_index_angle = calculate_angle(thumb_tip, index_tip, wrist)
            index_middle_angle = calculate_angle(index_tip, middle_tip, wrist)
            middle_ring_angle = calculate_angle(middle_tip, ring_tip, wrist)
            ring_pinky_angle = calculate_angle(ring_tip, pinky_tip, wrist)

            wrist_index_angle = calculate_angle(wrist, index_tip, index_mcp)
            wrist_middle_angle = calculate_angle(wrist, middle_tip, middle_mcp)
            wrist_ring_angle = calculate_angle(wrist, ring_tip, ring_mcp)
            wrist_pinky_angle = calculate_angle(wrist, pinky_tip, pinky_mcp)

            if is_hand_upward(landmarks):
                if hand_label == "Left":
                    left_orientation = "upward"
                    print("left hand is upward")
                else:
                    right_orientation = "upward"
                    print("right hand is upward")

            if is_hand_leftward(landmarks):
                if hand_label == "Left":
                    left_orientation = "leftward"
                    print("left hand is leftward")
                else:
                    right_orientation = "leftward"
                    print("right hand is leftward")

            if is_hand_rightward(landmarks):
                if hand_label == "Left":
                    left_orientation = "rightward"
                    print("left hand is rightward")
                else:
                    right_orientation = "rightward"
                    print("right hand is rightward")

            if hand_label == "Left":
                if left_orientation == "upward":
                    # if is_left_fist(hand.landmark, self.mp_hands):
                    #     left_fist = True
                    if is_flat_open_hand(landmarks, self.mp_hands):
                        left_open = True
                    tip_ids = [4, 8, 12, 16, 20]
                    finger_states = []
                    for tip_id in tip_ids:
                        finger_tip = landmarks[tip_id]
                        finger_mcp = landmarks[tip_id - 1]
                        if tip_id == 4:
                            finger_states.append(finger_tip.x < finger_mcp.x)
                        else:
                            finger_states.append(finger_tip.y < finger_mcp.y)

                    if finger_states[0] and not any(finger_states[1:]):
                        hand_gesture = "Swipe Left"
                if (
                    (self.prev_left_orientation == "leftward" and left_orientation == "rightward") or
                    (self.prevprev_left_orientation == "leftward" and self.prev_left_orientation == "rightward" and left_orientation == "rightward") or
                    (self.prevprev_left_orientation == "leftward" and self.prev_left_orientation == "upward" and left_orientation == "rightward")
                ):
                    hand_gesture = "Swipe Right"
                elif (
                    (self.prev_left_orientation == "rightward" and left_orientation == "leftward") or
                    (self.prevprev_left_orientation == "rightward" and self.prev_left_orientation == "leftward" and left_orientation == "leftward") or
                    (self.prevprev_left_orientation == "rightward" and self.prev_left_orientation == "upward" and left_orientation == "leftward")
                ):
                    hand_gesture = "Swipe Left"
                self.prevprev_left_orientation = self.prev_left_orientation
                self.prev_left_orientation = left_orientation
            elif hand_label == "Right":
                if right_orientation == "leftward":
                    tip_ids = [4, 8, 12, 16, 20]
                    finger_states = []
                    for tip_id in tip_ids:
                        finger_tip = landmarks[tip_id]
                        finger_mcp = landmarks[tip_id - 1]
                        if tip_id == 4:
                            finger_states.append(finger_tip.y < finger_mcp.y)
                        else:
                            finger_states.append(finger_tip.x < finger_mcp.x)
                    finger_count = finger_states.count(True)
                    if finger_count >= 1 and finger_count <= 5:
                        hand_gesture = f"Option {finger_count}"
                    else:
                        hand_gesture = "None"
                elif right_orientation == "upward":
                    # if is_right_fist(hand.landmark, self.mp_hands):
                    #     right_fist = True
                    if is_flat_open_hand(landmarks, self.mp_hands):
                        right_open = True
                    elif thumb_index_angle < 4 and index_middle_angle < 4 and middle_ring_angle < 5 and ring_pinky_angle < 4:
                        hand_gesture = "Zoom Out"
                    elif thumb_index_angle > 30 and index_middle_angle > 5 and middle_ring_angle > 5 and ring_pinky_angle > 10:
                        hand_gesture = "Zoom In"
                    elif wrist_index_angle > 160 and wrist_middle_angle < 25 and wrist_ring_angle < 20 and wrist_pinky_angle < 20:
                        # gesture = "Pointing"
                        index_tip_position = self.get_index_tip_position(hand_landmarks, frame.shape)
                        x, y = index_tip_position
                        # print(f"{x},{y}")
                        hand_gesture = "Pointing"
                        return f"{x},{y}"
                    else:
                        hand_gesture = "None"
                    tip_ids = [4, 8, 12, 16, 20]
                    finger_states = []
                    for tip_id in tip_ids:
                        finger_tip = landmarks[tip_id]
                        finger_mcp = landmarks[tip_id - 1]
                        if tip_id == 4:
                            finger_states.append(finger_tip.x > finger_mcp.x)
                        else:
                            finger_states.append(finger_tip.y < finger_mcp.y)
                    if finger_states[0] and not any(finger_states[1:]):
                        hand_gesture = "Swipe Right"

        if left_open and hand_gesture != "None":
            return hand_gesture
        elif not left_fist and hand_gesture == "Pointing":
            return "Drawing"
        elif right_open and hand_gesture != "None":
            return hand_gesture
        else:
            return "None"
