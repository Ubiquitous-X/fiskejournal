from ninja import Router, File
from ninja.files import UploadedFile
from django.http import JsonResponse
from pathlib import Path
from django.views.decorators.csrf import csrf_protect
from core.tasks import process_photo_upload
from django.conf import settings
import shutil
import logging

router = Router()

UPLOAD_DIRECTORY = Path(settings.BASE_DIR) / "uploads"

# Skapa uppladdningskatalogen om den inte finns
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Konfigurera logger
logger = logging.getLogger(__name__)

# Funktion för att kontrollera filtyp
def is_valid_filetype(file):
    valid_filetypes = ["image/jpeg", "image/heic", "image/heif"]
    return file.content_type in valid_filetypes

@csrf_protect
@router.post("/upload", auth=None)
def upload_file(request, file: UploadedFile = File(...)):
    if not request.user.is_authenticated:
        logger.warning("Uppladdningsförsök av ej inloggad användare")
        return JsonResponse({"detail": "Du är inte inloggad", "notification_type": "error"}, status=401)

    if not is_valid_filetype(file):
        logger.warning(f"Felaktig filtyp: {file.content_type}")
        return JsonResponse({"detail": "Felaktig filtyp", "notification_type": "error"}, status=400)

    file_location = UPLOAD_DIRECTORY / file.name
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file, buffer)
    except Exception as e:
        logger.error(f"Fel vid filuppladdningen: {e}")
        return JsonResponse({"detail": "Internt serverfel", "notification_type": "error"}, status=500)

    # Skicka filuppladdningen till Celery för vidare bearbetning
    process_photo_upload.delay(request.user.id, str(file_location))
    logger.info(f"Fil uppladdad av användare {request.user.username}: {file.name}")

    return JsonResponse({"message": "Fotot mottaget", "notification_type": "info"}, status=200)
