import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Navigation, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { Typography, Box, Container, List, ListItem, ListItemText, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';

const HomePage = () => {
    const { t } = useTranslation();

    return (
        <div>
            <Swiper
                modules={[Autoplay, Navigation, Pagination]}
                spaceBetween={30}
                slidesPerView={1}
                navigation
                pagination={{ clickable: true }}
                autoplay={{ delay: 3000, disableOnInteraction: false }}
                loop={true}
                style={{ maxHeight: '500px' }}
            >
                <SwiperSlide>
                    <img
                        src="https://blogassets.leverageedu.com/blog/wp-content/uploads/2020/03/24185535/Online-Learning.jpg"
                        style={{ width: '100%', objectFit: 'cover', maxHeight: '700px' }}
                    />
                </SwiperSlide>
                <SwiperSlide>
                    <img
                        src="https://www.keg.com/hubfs/shutterstock_404189197%20%281%29-1.jpg"
                        style={{ width: '100%', objectFit: 'cover', maxHeight: '500px' }}
                    />
                </SwiperSlide>
                <SwiperSlide>
                    <img
                        src="https://img-cdn.inc.com/image/upload/f_webp,q_auto,c_fit/images/panoramic/GettyImages-1217591630_449017_txf4as.jpg"
                        style={{ width: '100%', objectFit: 'cover', maxHeight: '500px' }}
                    />
                </SwiperSlide>
            </Swiper>

            <Container sx={{ mt: 8, mb: 8 }}>
                <Box
                    sx={{
                        textAlign: 'center',
                        mb: 6,
                        px: { xs: 2, md: 10 },
                    }}
                >
                    <Typography
                        variant="h3"
                        component="h1"
                        fontWeight="bold"
                        sx={{
                            mb: 2,
                            background: 'linear-gradient(to right, #007aff, #00c6ff)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                        }}
                    >
                        Gesture Vision AI
                    </Typography>
                    <Typography variant="h5" fontWeight="medium" gutterBottom>
                        {t('homePage.subtitle')}
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                        {t('homePage.subsubtitle')}
                    </Typography>
                </Box>

                <Box
                    sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 4,
                        maxWidth: 900,
                        mx: 'auto',
                        px: { xs: 2, md: 4 },
                    }}
                >
                    <Paper elevation={3} sx={{ p: 4, borderRadius: 4 }}>
                        <Typography variant="h6" fontWeight="bold" sx={{ mb: 2 }}>
                            🎯 {t('homePage.functions')}
                        </Typography>
                        <List>
                            <ListItem>
                                <ListItemText
                                    primary={`👉 ${t('homePage.func1Title')}`}
                                    secondary={t('homePage.func1Description')}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary={`🎥 ${t('homePage.func2Title')}`}
                                    secondary={t('homePage.func2Description')}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary={`🔍 ${t('homePage.func3Title')}`}
                                    secondary={t('homePage.func3Description')}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary={`⚙️ ${t('homePage.func4Title')}`}
                                    secondary={t('homePage.func4Description')}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary={`🖥️ ${t('homePage.func5Title')}`}
                                    secondary={t('homePage.func5Description')}
                                />
                            </ListItem>
                        </List>
                    </Paper>

                    <Paper elevation={2} sx={{ p: 4, borderRadius: 4, backgroundColor: '#f5faff' }}>
                        <Typography variant="h6" fontWeight="bold" sx={{ mb: 2 }}>
                            👨‍🏫 {t('homePage.question')}
                        </Typography>
                        <Typography variant="body1" dangerouslySetInnerHTML={{ __html: t('homePage.benefits') }} />
                    </Paper>
                </Box>
            </Container>
        </div>
    );
};

export default HomePage;
