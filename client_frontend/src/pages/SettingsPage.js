import { Box, Divider, Typography, Paper, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import { useState, useEffect } from "react";
import { useTranslation } from 'react-i18next';
import { getGestures, getOptions, defaultSettings } from "../utils/gestureOptions";

const SettingsPage = () => {
    const { t } = useTranslation();

    const Gestures = getGestures(t);
    const Options = getOptions(t);

    const [settings, setSettings] = useState({});

    useEffect(() => {
        const storedSettings = sessionStorage.getItem("gestureSettings");
        if (storedSettings) {
            setSettings(JSON.parse(storedSettings));
        } else {
            setSettings(defaultSettings);
            sessionStorage.setItem("gestureSettings", JSON.stringify(defaultSettings));
        }
    }, []);

    const handleChange = (gesture, action) => {
        const newSettings = { ...settings, [gesture.name]: action };
        setSettings(newSettings);
        sessionStorage.setItem("gestureSettings", JSON.stringify(newSettings));
    };

    const selectedOptions = Object.values(settings);

    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '80vh'
            }}
        >
            <Paper
                elevation={4}
                sx={{
                    width: '30%',
                    padding: '24px',
                    borderRadius: '12px',
                    backgroundColor: '#f9f9f9'
                }}
            >
                <Typography variant="h5" fontWeight="bold" textAlign="center" marginBottom={2}>
                    {t('settingsPage.title')}
                </Typography>
                <Divider sx={{ marginBottom: 2 }} />
                {Gestures.map((gesture) => (
                    <Box key={gesture.name} sx={{ marginBottom: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <Typography fontWeight="bold" sx={{ flex: 1 }}>
                                {gesture.name}
                            </Typography>
                            <FormControl size="small" sx={{ width: '40%' }}>
                                <InputLabel id={`${gesture.name}-label`}>{t('settingsPage.chooseOption')}</InputLabel>
                                <Select
                                    labelId={`${gesture.name}-label`}
                                    value={settings[gesture.name] || ""}
                                    onChange={(e) => handleChange(gesture, e.target.value)}
                                    label={t('settingsPage.chooseOption')}
                                    sx={{
                                        width: '100%',
                                        padding: '4px',
                                        fontSize: '0.875rem',
                                        height: '35px',
                                    }}
                                >
                                    <MenuItem value="">{t('settingsPage.chooseOption')}</MenuItem>
                                    {Options
                                        .filter((option) => !selectedOptions.includes(option) || settings[gesture.name] === option)
                                        .map((option) => (
                                            <MenuItem key={option} value={option}>
                                                {option}
                                            </MenuItem>
                                        ))}
                                </Select>
                            </FormControl>
                        </Box>
                        <Divider sx={{ marginTop: 1 }} />
                    </Box>
                ))}
            </Paper>
        </Box>
    );
};

export default SettingsPage;
