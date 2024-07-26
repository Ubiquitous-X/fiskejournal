from celery import shared_task
from celery.utils.log import get_task_logger
from api.models import Fish, FishSpecies
from django.contrib.auth.models import User
from django.utils import timezone as dj_timezone
from PIL import Image
from core.task_functions.utils import send_notification
from core.task_functions.api_clients import get_fish_species, get_location_name, get_current_weather_data
from core.task_functions.aws_utils import upload_to_s3, delete_images_from_s3
from core.task_functions.image_processing import extract_exif_data, convert_and_resize_image
import piexif
import os

# Konfigurera logger
logger = get_task_logger(__name__)

@shared_task
def process_photo_upload(user_id, file_path):
    # Hämta användare
    user = User.objects.get(id=user_id)

    # Öppna den lokala filen
    img = Image.open(file_path)

    # Försök att extrahera EXIF-data från fotot
    exif_dict = img.info.get('exif')
    if exif_dict:
        try:
            exif_dict = piexif.load(exif_dict)
            metadata = extract_exif_data(exif_dict)

            # Hämta tidsstämpel, latitud och longitud från metadata
            timestamp = metadata['DateTimeOriginal']
            latitude = metadata['GPSLatitude']
            longitude = metadata['GPSLongitude']

            # Avrunda latitud och longitud till 4 decimaler
            latitude = round(latitude, 4)
            longitude = round(longitude, 4)

        except Exception as e:
            logger.error(f"Fel vid bearbetning av EXIF-data: {e}")
            os.remove(file_path)

            # Skicka meddelande om felaktig metadata
            send_notification(f'Det saknas metadata', 'error', delay=1)
            return
    else:
        logger.error(f"Ingen EXIF-data hittades i {file_path}")
        os.remove(file_path)

        # Skicka meddelande om felaktig metadata
        send_notification('Ingen EXIF-data hittades', 'error', delay=1)
        return

    # Gör datetime-objektet tidszon-aware med Djangos aktuella tidszon
    current_tz = dj_timezone.get_current_timezone()
    timestamp = dj_timezone.make_aware(timestamp, current_tz)

    # Kontrollera om det redan finns ett foto med samma tidsstämpel
    if Fish.objects.filter(timestamp=timestamp).exists():
        logger.error(f"En fisk med tidsstämpeln {timestamp} finns redan i databasen")
        os.remove(file_path)
        # Skicka meddelande om existerande foto
        send_notification('Detta foto finns redan', 'error', delay=1)
        return

    # Skapa fiskobjektet och sätt de obligatoriska fälten
    fish = Fish(
        timestamp=timestamp,
        latitude=latitude,
        longitude=longitude,
        fisherman=user
    )

    # Hämta platsdata och uppdatera fiskobjektet
    location_name = get_location_name(latitude, longitude)

    # Kontrollera och omvandla "Ulvhällsfjärd" till "Ulvhällsfjärden"
    if location_name == "Ulvhällsfjärd":
        location_name = "Ulvhällsfjärden"

    fish.location = location_name

    # Hämta väderdata och uppdatera fiskobjektet
    weather_data = get_current_weather_data(latitude, longitude)
    if weather_data[0] is not None:
        (weather, air_temperature, air_pressure, wind_speed, wind_dir, uv_index,
         moon_phase, moon_illumination, air_humidity, weather_icon_url) = weather_data

        fish.weather = weather
        fish.air_temperature = air_temperature
        fish.air_pressure = air_pressure
        fish.wind_speed = wind_speed
        fish.wind_dir = wind_dir
        fish.uv_index = uv_index
        fish.moon_phase = moon_phase
        fish.moon_illumination = moon_illumination
        fish.air_humidity = air_humidity
        fish.weather_icon_url = weather_icon_url

    # Skapa flera storlekar
    base_path, ext = os.path.splitext(file_path)
    medium_path = f"{base_path}_800.jpg"
    thumb_path = f"{base_path}_150.jpg"

    convert_and_resize_image(file_path, medium_path, 800)
    convert_and_resize_image(file_path, thumb_path, 150)

    # Ladda upp bilderna till S3 och spara URL:erna i databasen
    medium_url = upload_to_s3(medium_path, user.username, timestamp, 'medium')
    thumb_url = upload_to_s3(thumb_path, user.username, timestamp, 'thumb')

    # Skicka meddelande om fotouppladdning
    send_notification('Fotot konverterat', 'info')

    fish.medium_image_url = medium_url
    fish.thumbnail_image_url = thumb_url

    # Anropa OpenAI API för artbestämning
    species_name = get_fish_species(medium_path)

    # Kontrollera om arten finns i FishSpecies, annars sätt till "Ej bestämd"
    species = FishSpecies.objects.filter(name=species_name).first()
    if not species:
        species = FishSpecies.objects.get(name="Ej bestämd")

    fish.species = species

    # Skicka meddelande om artbestämning
    send_notification(f'Identifierad som: {species.name}', 'info', delay=1)
    send_notification(f'Fångstplats: {location_name}', 'info', delay=0.5)
    # Spara fiskobjektet
    fish.save()

    # Radera den lokala filen och de konverterade bilderna
    os.remove(file_path)
    os.remove(medium_path)
    os.remove(thumb_path)

    # När bearbetningen är klar, skicka ett meddelande
    send_notification('Fotot är färdigbehandlat!', 'success', delay=1)


@shared_task
def delete_fish_images_from_s3(image_urls):
    return delete_images_from_s3(image_urls)
