import cv2
import subprocess
import threading
import time

RTSP_RECEIVE_URL = "rtsp://127.0.0.1:8554/stream"

def start_streaming():
    gst_command = [
        "gst-launch-1.0", "avfvideosrc", "!", "videoconvert", "!", "x264enc", "tune=zerolatency", "!", 
        "rtph264pay", "config-interval=1", "pt=96", "!", "udpsink", "host=127.0.0.1", "port=5000"
    ]
    subprocess.Popen(gst_command)

def receive_stream():
    cap = cv2.VideoCapture(RTSP_RECEIVE_URL)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("error: can not read stream")
            break
        cv2.imshow("RTSP stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

stream_thread = threading.Thread(target=start_streaming)
stream_thread.start()

receive_stream()
