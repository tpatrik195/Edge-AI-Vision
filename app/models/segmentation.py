# import cv2
# import mediapipe as mp
# import numpy as np

# class BackgroundSegmenter:
#     def __init__(self, background_image_path):
#         self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
#         self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
#         self.background = cv2.imread(background_image_path)

#     def segment_background(self, frame):
#         h, w, _ = frame.shape
#         self.background = cv2.resize(self.background, (w, h))

#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result_seg = self.segmentation.process(frame_rgb)
#         mask = result_seg.segmentation_mask[:, :, np.newaxis]

#         return (frame * mask + self.background * (1 - mask)).astype(np.uint8)



import cv2
import mediapipe as mp
import numpy as np

class BackgroundSegmenter:
    def __init__(self, background_image):
        """
        A konstruktor most már közvetlenül képadatot vár, nem fájlútvonalat.
        :param background_image: A háttérkép, amit szegmentáláshoz használunk (NumPy tömb).
        """
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
        
        # Ha a háttér képadatot kapott, azt közvetlenül használjuk
        if isinstance(background_image, np.ndarray):
            self.background = background_image
        else:
            raise ValueError("The background must be a valid image array (NumPy array).")

    def segment_background(self, frame):
        """
        Szegmentálja a háttér és a kép közötti különbséget és alkalmazza a háttérképhez.
        :param frame: A szegmentálásra váró képkép (NumPy tömb).
        :return: A szegmentált kép.
        """
        h, w, _ = frame.shape
        
        # Ha a háttérkép nem megfelelő méretű, átméretezzük a képkocka méretéhez
        self.background = cv2.resize(self.background, (w, h))  # Módosított háttér mérete
        
        # Kép RGB-re konvertálása, hogy Mediapipe dolgozni tudjon vele
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_seg = self.segmentation.process(frame_rgb)
        
        # Maszk kinyerése és bővítése, hogy illeszkedjen a frame-hez
        mask = result_seg.segmentation_mask[:, :, np.newaxis]  # Eredeti maszk (egyszínű)
        # mask = np.repeat(mask, 3, axis=2)  # Átalakítjuk 3 csatornás maszkra
        
        # A szegmentált kép visszaadása
        # A maszk segítségével a háttér és a frame kombinálása
        return (frame * mask + self.background * (1 - mask)).astype(np.uint8)
