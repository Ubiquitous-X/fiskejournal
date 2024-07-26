from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from typing import List
from django.views.decorators.csrf import csrf_protect
from ninja.security import django_auth
from api.models import Bait
from api.schemas import BaitOut, BaitCreate

router = Router()

@router.get("/all", response=List[BaitOut])
def get_all_baits(request) -> QuerySet[Bait]:
    baits = Bait.objects.all().order_by('type')
    return baits

@router.post("/", response=BaitOut, auth=django_auth)
def create_bait(request, payload: BaitCreate):
    bait = Bait.objects.create(**payload.dict())
    return bait

@csrf_protect
@router.put("/edit/{bait_id}", response=BaitOut, auth=django_auth)
def update_bait(request, bait_id: int, payload: BaitCreate):
    bait = get_object_or_404(Bait, id=bait_id)
    for attr, value in payload.dict().items():
        setattr(bait, attr, value)
    bait.save()
    return bait

@csrf_protect
@router.delete("/delete/{bait_id}", auth=django_auth)
def delete_bait(request, bait_id: int):
    bait = get_object_or_404(Bait, id=bait_id)
    bait.delete()
    return {"message": "Bete raderat"}
