from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from ninja.security import django_auth
from django.views.decorators.csrf import csrf_protect
from typing import List
from api.models import Fish, FishSpecies, Bait
from api.schemas import FishCreate, FishOut, FishUpdate
from core.tasks import delete_fish_images_from_s3

router = Router()

@router.get("/all", response=List[FishOut])
def get_all_fish(request) -> QuerySet[Fish]:
    fish_list = Fish.objects.all().order_by('-timestamp')
    return fish_list

@router.get("/{slug}", response=FishOut)
def get_fish(request, slug: str):
    fish = get_object_or_404(Fish, slug=slug)
    return fish

@csrf_protect
@router.post("/", response=FishOut, auth=django_auth)
def create_fish(request, payload: FishCreate):
    fish = Fish.objects.create(**payload.dict())
    return fish

@csrf_protect
@router.put("/edit/{fish_id}", response=FishOut, auth=django_auth)
def update_fish(request, fish_id: int, payload: FishUpdate):
    fish = get_object_or_404(Fish, id=fish_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr == 'species':
            fish.species = get_object_or_404(FishSpecies, id=value)
        elif attr == 'bait':
            fish.bait = get_object_or_404(Bait, id=value) if value is not None else None
        else:
            setattr(fish, attr, value)
    fish.save()
    return fish

@csrf_protect
@router.delete("/delete/{fish_id}", auth=django_auth)
def delete_fish(request, fish_id: int):
    fish = get_object_or_404(Fish, id=fish_id)

    # Hämta bild-URL:er innan objektet raderas
    image_urls = [fish.medium_image_url, fish.thumbnail_image_url]

    # Radera fisken från databasen
    fish.delete()

    # Anropa tasken för att radera bilder från S3
    delete_fish_images_from_s3.delay(image_urls)

    return {"message": "Fisken raderad"}
