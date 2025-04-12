import React, { useRef, useEffect, useState } from "react";
import Webcam from "react-webcam";
import { io } from "socket.io-client";
import { useTranslation } from "react-i18next";
import { useNavigate, useLocation } from "react-router-dom";
import "../App.css";

const SERVER_URL = "http://127.0.0.1:8000";
const WEBHOOK_URL = "http://127.0.0.1:9000/webhook";
const socket = io("http://localhost:9000");

const GestureDetailPage = () => {
    const webcamRef = useRef(null);
    const frameInterval = useRef(null);
    const [gesture, setGesture] = useState("");
    const { t } = useTranslation();
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        socket.on("gesture_event", (data) => {
            console.log("Gesture received from WebSocket:", data);
            setGesture(data.gesture);
        });

        return () => {
            socket.off("gesture_event");
        };
    }, []);

    const startFrameStreaming = () => {
        frameInterval.current = setInterval(async () => {
            if (webcamRef.current && webcamRef.current.video.readyState === 4) {
                const video = webcamRef.current.video;
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");

                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                canvas.toBlob(async (blob) => {
                    if (blob) {
                        const formData = new FormData();
                        formData.append("frame", blob, "frame.jpg");

                        try {
                            await fetch(`${SERVER_URL}/process_frame`, {
                                method: "POST",
                                body: formData,
                            });
                        } catch (error) {
                            console.error("Error sending frame", error);
                        }
                    }
                }, "image/jpeg");
            }
        }, 100);
    };

    const subscribeToWebhook = async () => {
        try {
            const response = await fetch(`${SERVER_URL}/subscribe_webhook?url=${WEBHOOK_URL}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            if (!response.ok) {
                throw new Error(`Subscription failed with status ${response.status}`);
            }

            console.log("Successfully subscribed to webhook.");
        } catch (error) {
            console.error("Webhook subscription failed", error);
        }
    };

    const unsubscribeFromWebhook = async () => {
        try {
            const response = await fetch(`${SERVER_URL}/unsubscribe_webhook?url=${WEBHOOK_URL}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ url: WEBHOOK_URL }),
            });

            if (!response.ok) {
                throw new Error(`Subscription failed with status ${response.status}`);
            }

            stopFrameStreaming();
        } catch (error) {
            console.error("Unsubscription failed", error);
        }
    };

    const stopFrameStreaming = () => {
        if (frameInterval.current) {
            clearInterval(frameInterval.current);
            frameInterval.current = null;
        }
    };

    useEffect(() => {
        subscribeToWebhook();
        startFrameStreaming();

        return () => {
            if (location.pathname.startsWith("/practice/")) {
                console.log("Leaving /practice/:gestureId, unsubscribing from webhook...");
                unsubscribeFromWebhook();
            }
        };
    }, [location.pathname]);

    return (
        <div className="container" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "85vh" }}>
            <Webcam ref={webcamRef} style={{ width: "100%", maxWidth: "840px", borderRadius: "10px" }} />
            <p style={{ marginTop: "10px", fontSize: "20px", fontWeight: "bold" }}>
                {t("presentationPage.recognizedGesture")} {gesture}
            </p>
        </div>
    );
};

export default GestureDetailPage;
