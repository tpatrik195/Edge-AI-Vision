from app.api.video_stream import RTSPServer

if __name__ == "__main__":
    server = RTSPServer()
    server.run()
