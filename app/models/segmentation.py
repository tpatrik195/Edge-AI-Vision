import cv2
import mediapipe as mp
import numpy as np

class BackgroundSegmenter:
    def __init__(self):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    def segment_background(self, frame):
        h, w, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_seg = self.segmentation.process(frame_rgb)
        mask = result_seg.segmentation_mask

        mask = (mask * 255).astype(np.uint8)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        _, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)

        mask = mask[:, :, np.newaxis]

        segmented_frame = (frame * (mask / 255)).astype(np.uint8)
        return segmented_frame
