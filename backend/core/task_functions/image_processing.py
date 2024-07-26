from celery.utils.log import get_task_logger
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
from datetime import datetime
from core.task_functions.utils import dms_to_dd
import pillow_heif
import piexif

# Konfigurera logger
logger = get_task_logger(__name__)

# Registrera HEIC/HEIF-läsaren för dessa bildformat
register_heif_opener()

def extract_exif_data(exif_dict):
    """Extrahera vald EXIF-data från EXIF-dictionary"""
    selected_tags = {
        piexif.ExifIFD.DateTimeOriginal: "DateTimeOriginal",
        piexif.GPSIFD.GPSLatitude: "GPSLatitude",
        piexif.GPSIFD.GPSLongitude: "GPSLongitude"
    }

    exif_data = {}

    for ifd in exif_dict:
        if ifd == "thumbnail":
            continue

        if exif_dict[ifd] is None:
            logger.warning(f"Hoppar över {ifd} eftersom det är None")
            continue

        for tag in exif_dict[ifd]:
            if tag in selected_tags:
                tag_name = selected_tags[tag]
                value = exif_dict[ifd][tag]
                try:
                    if tag_name == "DateTimeOriginal":
                        if isinstance(value, bytes):
                            value = value.decode('utf-8')
                        value = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        exif_data[tag_name] = value
                    elif tag_name in ["GPSLatitude", "GPSLongitude"]:
                        value = dms_to_dd(value) if isinstance(value, tuple) and len(value) == 3 else None
                        exif_data[tag_name] = value
                except Exception as e:
                    logger.error(f"Fel vid bearbetning av taggen {tag_name}: {e}")

    # Kontrollera om nödvändig EXIF-data saknas
    if 'DateTimeOriginal' not in exif_data:
        raise ValueError("Tidsstämpel saknas")
    if 'GPSLatitude' not in exif_data:
        raise ValueError("Latitud saknas")
    if 'GPSLongitude' not in exif_data:
        raise ValueError("Longitud saknas")

    return exif_data


def convert_and_resize_image(input_path, output_path, max_size):
    """Konvertera och ändra storlek på bilden till specificerad maxstorlek"""
    # Kontrollera filändelsen för att hantera HEIC separat
    if input_path.lower().endswith('.heic'):
        heif_file = pillow_heif.read_heif(input_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    else:
        image = Image.open(input_path)

    # Justera bildens orientering baserat på EXIF-data
    image = ImageOps.exif_transpose(image)

    # Beräkna ny storlek för att hålla proportioner
    ratio = min(max_size / image.width, max_size / image.height)
    new_size = (int(image.width * ratio), int(image.height * ratio))

    # Förminska bilden
    image = image.resize(new_size, Image.Resampling.LANCZOS)

    # Spara som .jpg
    image.save(output_path, format="JPEG")
