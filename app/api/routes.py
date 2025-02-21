from flask import Blueprint, request, jsonify
from .video_stream import VideoStreamHandler

api_bp = Blueprint('api', __name__)

@api_bp.route('/process_video', methods=['POST'])
def process_video():
    video_stream = request.stream
    handler = VideoStreamHandler(video_stream)
    processed_image = handler.process_video_stream()

    return jsonify({'processed_image': processed_image}), 200
