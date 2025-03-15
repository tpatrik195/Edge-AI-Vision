import cv2
import mediapipe as mp
import numpy as np

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
