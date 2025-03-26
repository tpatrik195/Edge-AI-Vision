import { useEffect } from "react";
import { defaultSettings } from "../utils/gestureOptions";

const HomePage = () => {
    useEffect(() => {
        const storedSettings = sessionStorage.getItem("gestureSettings");
        if (!storedSettings) {
            sessionStorage.setItem("gestureSettings", JSON.stringify(defaultSettings));
        }
    }, []);

    return (
        <div>
            <p>
                home page
            </p>
        </div>
    );
}

export default HomePage;
