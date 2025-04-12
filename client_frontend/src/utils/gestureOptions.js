export const getGestures = (t) => [
    { id: 1, name: t('settingsPage.option1'), image: '' },
    { id: 2, name: t('settingsPage.option2'), image: '' },
    { id: 3, name: t('settingsPage.option3'), image: '' },
    { id: 4, name: t('settingsPage.option4'), image: '' },
    { id: 5, name: t('settingsPage.option5'), image: '' },
    { id: 6, name: t('settingsPage.zoomIn'), image: '' },
    { id: 7, name: t('settingsPage.zoomOut'), image: '' },
    { id: 8, name: t('settingsPage.swipeLeft'), image: '' },
    { id: 9, name: t('settingsPage.swipeRight'), image: '' },
];

export const getOptions = (t) => [
    t('presentationPage.fullScreen'),
    t('presentationPage.showPerson'),
    t('presentationPage.hidePerson'),
    t('settingsPage.exitFullScreen'),
    t('settingsPage.zoomIn'),
    t('settingsPage.zoomOut'),
    t('settingsPage.swipeLeft'),
    t('settingsPage.swipeRight')
];

export const defaultSettings = {
    "Zoom In": "Zoom In",
    "Zoom Out": "Zoom Out",
    "Swipe Left": "Swipe Left",
    "Swipe Right": "Swipe Right"
};