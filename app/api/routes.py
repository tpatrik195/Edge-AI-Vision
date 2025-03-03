from flask import Blueprint, request, jsonify, Response
from app.api.video_stream import process_rtsp_stream
from app.api.process import process_frame
import cv2

# Blueprint létrehozása
api = Blueprint("api", __name__)

# Egyszerű teszt endpoint
@api.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "API is running"}), 200

# RTSP stream fogadása és feldolgozása
@api.route("/process_video", methods=["POST"])
def process_video():
    """
    RTSP URL-t fogad, végrehajtja az AI alapú feldolgozást, és visszaküldi a streamet.
    """
    data = request.get_json()
    rtsp_url = data.get("rtsp_url")

    if not rtsp_url:
        return jsonify({"error": "RTSP URL is required"}), 400

    # Stream feldolgozása
    return Response(process_rtsp_stream(rtsp_url), mimetype="multipart/x-mixed-replace; boundary=frame")

# Egyetlen kép feldolgozása (pl. fájlfeltöltés esetén)
@api.route("/process_image", methods=["POST"])
def process_image():
    """
    Feltöltött képet fogad és AI feldolgozást végez rajta.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file found"}), 400

    file = request.files["image"]
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    processed_image = process_frame(image)

    _, buffer = cv2.imencode(".jpg", processed_image)
    return Response(buffer.tobytes(), mimetype="image/jpeg")
