import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from core.task_functions.utils import send_notification
from celery.utils.log import get_task_logger

# Hämta AWS-uppgifter från miljövariabler
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# Konfigurera logger
logger = get_task_logger(__name__)

# Skapa en S3-klient för interaktion med AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)

def upload_to_s3(file_path, user_name, timestamp, size):
    """Ladda upp filen till S3 och returnera URL:en"""
    upload_directory = os.getenv('AWS_UPLOAD_DIRECTORY', 'foton')
    formatted_date = timestamp.strftime('%y%m%d-%H%M')
    s3_key = f"{upload_directory}/{formatted_date}-{user_name}-{size}.jpg"

    try:
        s3_client.upload_file(
            file_path,
            AWS_STORAGE_BUCKET_NAME,
            s3_key,
            ExtraArgs={"ContentType": "image/jpeg"}
        )
        return f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}"
    except NoCredentialsError:
        logger.error("AWS-autentisering misslyckades")
        send_notification(f'Kunde ej ladda upp till S3', 'error', delay=1)
    except ClientError as e:
        logger.error(f"Fel vid filuppladdningen: {e}")
        send_notification(f'Kunde ej ladda upp till S3', 'error', delay=1)
        return None

def delete_images_from_s3(image_urls):
    """Radera bilder från S3 baserat på URL:er"""
    all_deleted = True  # Flagga för att hålla koll på om alla raderingar lyckades
    for url in image_urls:
        try:
            bucket_name = url.split('/')[2].split('.')[0]
            key = '/'.join(url.split('/')[3:])

            s3_client.delete_object(Bucket=bucket_name, Key=key)
        except NoCredentialsError:
            logger.error("AWS-autentisering misslyckades")
            send_notification(f'Kunde ej radera från S3', 'error', delay=1)
            all_deleted = False  # Sätt flaggan till False om det misslyckas
        except ClientError as e:
            logger.error(f"Fel vid borttagning av fil: {e}")
            send_notification(f'Kunde ej radera från S3', 'error', delay=1)
            all_deleted = False  # Sätt flaggan till False om det misslyckas

    # Skicka notifikation en gång om alla raderingar lyckades
    if all_deleted:
        send_notification(f'Foton raderade från S3', 'info', delay=1)

    return all_deleted
