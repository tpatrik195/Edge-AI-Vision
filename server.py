import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class RTSPMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super(RTSPMediaFactory, self).__init__()
        self.set_launch(
            "udpsrc port=5000 caps=\"application/x-rtp,media=video,clock-rate=90000,encoding-name=H264\" ! "
            "rtph264depay ! decodebin ! videoconvert ! x264enc tune=zerolatency ! "
            "rtph264pay config-interval=1 pt=96 name=pay0"
        )
        self.set_shared(True)

class RTSPServer(GstRtspServer.RTSPServer):
    def __init__(self):
        super(RTSPServer, self).__init__()
        self.factory = RTSPMediaFactory()
        self.get_mount_points().add_factory("/stream", self.factory)
        self.attach(None)
        print("RTSP server run on:  rtsp://127.0.0.1:8554/stream")

Gst.init(None)
server = RTSPServer()

loop = GObject.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    print("server stop")
