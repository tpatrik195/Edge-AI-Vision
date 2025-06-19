import React, { useEffect, useRef, useState } from "react";

const CursorFollower = ({ markerPosition }) => {
    const cursorRef = useRef(null);

    useEffect(() => {
        if (markerPosition && cursorRef.current) {
            cursorRef.current.style.transform = `translate(${markerPosition.x}px, ${markerPosition.y}px)`;
        }
    }, [markerPosition]);

    return (
        <div
            ref={cursorRef}
            style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "20px",
                height: "20px",
                borderRadius: "50%",
                backgroundColor: "red",
                pointerEvents: "none",
                transition: "transform 0.1s linear",
                zIndex: 9999,
            }}
        />
    );
};

export default CursorFollower;
