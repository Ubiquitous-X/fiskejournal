from django.contrib import admin
from .models import Fish, FishSpecies, Bait

@admin.register(Fish)
class FishAdmin(admin.ModelAdmin):
    list_display = ('species', 'timestamp', 'location')
    search_fields = ('species__name',)

@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'latin_name')
    search_fields = ('name', 'latin_name')

@admin.register(Bait)
class BaitAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)
