import React from 'react';
import PracticeCard from "../components/PracticeCard";
import { getGestures } from "../utils/gestureOptions";
import { useTranslation } from 'react-i18next';
import { Box } from '@mui/material';

const PracticePage = () => {
    const { t } = useTranslation();
    const gestures = getGestures(t);
    return (
        <Box style={{ display: 'flex', flexWrap: 'wrap' }}>
            {gestures.map((gesture, index) => (
                <PracticeCard key={index} id={gesture.id} name={gesture.name} image={gesture.image} t={t} />
            ))}
        </Box>
    );
};

export default PracticePage;
