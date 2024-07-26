from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from ninja.security import django_auth
from django.views.decorators.csrf import csrf_protect
from typing import List
from api.models import FishSpecies, Fish
from api.schemas import FishSpeciesOut, FishSpeciesCreate

router = Router()

@router.get("/all", response=List[FishSpeciesOut])
def get_all_fish_species(request) -> QuerySet[FishSpecies]:
    species = FishSpecies.objects.all().order_by('name')
    return species

@csrf_protect
@router.post("/", response=FishSpeciesOut, auth=django_auth)
def create_fish_species(request, payload: FishSpeciesCreate):
    species = FishSpecies.objects.create(**payload.dict())
    return species

@csrf_protect
@router.put("/edit/{species_id}", response=FishSpeciesOut, auth=django_auth)
def update_fish_species(request, species_id: int, payload: FishSpeciesCreate):
    species = get_object_or_404(FishSpecies, id=species_id)
    for attr, value in payload.dict().items():
        setattr(species, attr, value)
    species.save()
    return species

@csrf_protect
@router.delete("/delete/{species_id}", auth=django_auth)
def delete_fish_species(request, species_id: int):
    species = get_object_or_404(FishSpecies, id=species_id)

    # Kontrollera om det finns några relaterade Fish-objekt
    related_fish_count = Fish.objects.filter(species=species).count()
    if related_fish_count > 0:
        return {"error": "Kan ej raderas, det finns fiskar av arten"}

    species.delete()
    return {"message": "Arten raderad"}
