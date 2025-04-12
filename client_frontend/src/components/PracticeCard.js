import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import CardActionArea from '@mui/material/CardActionArea';
import CardActions from '@mui/material/CardActions';

const SERVER_URL = "http://127.0.0.1:8000";
const WEBHOOK_URL = "http://127.0.0.1:9000/webhook";

export default function PracticeCard({ id, name, image, t }) {
  const navigate = useNavigate();

  const subscribeToWebhook = async () => {
    try {
      await fetch(`${SERVER_URL}/subscribe_webhook?url=${WEBHOOK_URL}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      navigate(`/practice/${id}`);
    } catch (error) {
      console.error("Webhook subscription failed", error);
    }
  };

  return (
    <Card sx={{ width: 350, height: 300, margin: 3 }} onClick={subscribeToWebhook}>
      <CardActionArea>
        <CardMedia component="img" height="185" image={image || ''} alt={name} />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {name}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="grey">
          {t('practiceCard.tryGesture')}
        </Button>
      </CardActions>
    </Card>
  );
}
