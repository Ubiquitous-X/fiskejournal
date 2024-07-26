# auth.py
from ninja import Router
from pydantic import BaseModel
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.http import HttpRequest

class AuthPayload(BaseModel):
    username: str
    password: str

router = Router()

@csrf_protect
@router.post("/login")
def login_view(request: HttpRequest, payload: AuthPayload):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Inloggning lyckades"}, status=200)
    else:
        return JsonResponse({"message": "Fel användarnamn eller lösenord"}, status=401)

@csrf_protect
@router.post("/logout")
def logout_view(request: HttpRequest):
    logout(request)
    return JsonResponse({"message": "Du är nu utloggad"}, status=200)

@csrf_protect
@router.get("/status")
def status_view(request: HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({"is_logged_in": True, "username": request.user.username}, status=200)
    else:
        return JsonResponse({"is_logged_in": False}, status=200)

@router.get("/csrf-token")
@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})
