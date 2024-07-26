from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from api.endpoints.fish import router as fish_router
from api.endpoints.bait import router as bait_router
from api.endpoints.species import router as species_router
from api.endpoints.files import router as file_router
from api.endpoints.auth import router as auth_router
from api.endpoints.weather import router as weather_router

api = NinjaAPI()
api.add_router("/fish", fish_router)
api.add_router("/baits", bait_router)
api.add_router("/species", species_router)
api.add_router('/file', file_router)
api.add_router('/auth', auth_router)
api.add_router("/weather", weather_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
