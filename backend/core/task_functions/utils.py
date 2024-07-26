from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger
import time
import base64

# Konfigurera logger
logger = get_task_logger(__name__)

def send_notification(message, notification_type, delay=0):
    """
    Hjälpfunktion för att skicka WebSocket-meddelanden.

    :param message: Strängmeddelandet som ska skickas.
    :param notification_type: Typ av meddelande (success, error, info, warning).
    :param delay: Fördröjning i sekunder innan meddelandet skickas. Standard är 0.
    """
    if delay > 0:
        time.sleep(delay)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
            'notification_type': notification_type
        }
    )

def dms_to_dd(dms):
    """Konvertera grader, minuter, sekunder till decimalgrader"""
    try:
        degrees, minutes, seconds = dms
        dd = degrees[0] / degrees[1] + (minutes[0] / minutes[1]) / 60 + (seconds[0] / seconds[1]) / 3600
        return dd
    except (TypeError, ValueError) as e:
        logger.error(f"Fel vid konvertering av DMS till DD: {e}")
        return None


def encode_image(image_path):
    """Koda bilden till base64 för användande till OpenAI"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
