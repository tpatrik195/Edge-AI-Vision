import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

background = cv2.imread("pictures/background.jpg")

person_width = 320
person_height = 240

cap = cv2.VideoCapture(0)

normal_distance = 0.1
threshold_close = 0.07
threshold_far = 0.3

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, c = frame.shape

    background = cv2.resize(background, (w, h))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result_seg = segmentation.process(frame_rgb)
    mask = result_seg.segmentation_mask

    mask = mask[:, :, np.newaxis]
    frame_segmented = (frame * mask + background * (1 - mask)).astype(np.uint8)

    result_hands = hands.process(frame_rgb)

    result_pose = pose.process(frame_rgb)

    if result_hands.multi_hand_landmarks:
        for hand_landmarks in result_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_segmented, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            thumb_index_distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
            thumb_pinky_distance = np.sqrt((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2)

            if thumb_index_distance < threshold_close or thumb_pinky_distance < threshold_close:
                gesture = "-"
            elif thumb_index_distance > threshold_far or thumb_pinky_distance > threshold_far:
                gesture = "+"
            else:
                gesture = "normal"

            cv2.putText(frame_segmented, f'gesture: {gesture}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if result_pose.pose_landmarks:
        mp_drawing.draw_landmarks(frame_segmented, result_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('gesture detection', frame_segmented)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
