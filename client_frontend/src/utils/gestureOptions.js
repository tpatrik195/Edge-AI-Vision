import option1_image from '../pictures/option_1.png';
import option2_image from '../pictures/option_2.png';
import option3_image from '../pictures/option_3.png';
import option4_image from '../pictures/option_4.png';
import option5_image from '../pictures/option_5.png';
import zoom_in_image from '../pictures/zoom_in.png';
import zoom_out_image from '../pictures/zoom_out.png';
import swipe_left_image from '../pictures/swipe_left.png';
import swipe_right_image from '../pictures/swipe_right.png';
import laser_pointer_image from '../pictures/laser_pointer.png';

export const getGestures = (t) => [
    { id: 1, name: t('settingsPage.option1'), image: option1_image, description: t('practicePage.option1Description') },
    { id: 2, name: t('settingsPage.option2'), image: option2_image, description: t('practicePage.option2Description') },
    { id: 3, name: t('settingsPage.option3'), image: option3_image, description: t('practicePage.option3Description') },
    { id: 4, name: t('settingsPage.option4'), image: option4_image, description: t('practicePage.option4Description') },
    { id: 5, name: t('settingsPage.option5'), image: option5_image, description: t('practicePage.option5Description') },
    { id: 6, name: t('settingsPage.zoomIn'), image: zoom_in_image, description: t('practicePage.zoomInDescription') },
    { id: 7, name: t('settingsPage.zoomOut'), image: zoom_out_image, description: t('practicePage.zoomOutDescription') },
    { id: 8, name: t('settingsPage.swipeLeft'), image: swipe_left_image, description: t('practicePage.swipeLeftDescription') },
    { id: 9, name: t('settingsPage.swipeRight'), image: swipe_right_image, description: t('practicePage.swipeRightDescription') },
    { id: 10, name: t('settingsPage.laserPointer'), image: laser_pointer_image, description: t('practicePage.laserPointerDescription') },
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