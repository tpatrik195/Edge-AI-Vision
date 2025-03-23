import React, { useRef, useEffect, useState } from "react";
import Webcam from "react-webcam";
import { SelfieSegmentation } from "@mediapipe/selfie_segmentation";
import * as cam from "@mediapipe/camera_utils";
import DisplayLottie from "../DisplayLottie";
import loader from "../85646-loading-dots-blue.json";

const WebcamComponent = ({ imageURL }) => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const [load, setLoad] = useState(false);

  const onResults = (results) => {
    const canvasElement = canvasRef.current;
    const canvasCtx = canvasElement.getContext("2d");
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
    setLoad(true);
  };

  useEffect(() => {
    const selfieSegmentation = new SelfieSegmentation({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation/${file}`,
    });

    selfieSegmentation.setOptions({ modelSelection: 1 });
    selfieSegmentation.onResults(onResults);

    if (webcamRef.current) {
      const camera = new cam.Camera(webcamRef.current.video, {
        onFrame: async () => await selfieSegmentation.send({ image: webcamRef.current.video }),
        width: 1280,
        height: 720,
      });
      camera.start();
    }
  }, []);

  return (
    <div className="videoContainer">
      <Webcam ref={webcamRef} style={{ display: "none" }} />
      {!load && <DisplayLottie animationData={loader} />}
      <canvas ref={canvasRef} className="videoCanvas"></canvas>
    </div>
  );
};

export default WebcamComponent;
