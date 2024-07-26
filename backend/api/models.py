from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class FishSpecies(models.Model):
    name = models.CharField(max_length=100)
    latin_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Fish Species'

    def __str__(self):
        return self.name


class Bait(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Baits'

    def __str__(self):
        return self.type

class Fish(models.Model):
    medium_image_url = models.CharField(max_length=255)
    thumbnail_image_url = models.CharField(max_length=255)
    timestamp = models.DateTimeField(db_index=True)
    species = models.ForeignKey(FishSpecies, on_delete=models.CASCADE)
    location = models.CharField(db_index=True, max_length=255, null=True, blank=True)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    weather = models.CharField(max_length=255, null=True, blank=True)
    weather_icon_url = models.CharField(max_length=255, null=True, blank=True)
    air_temperature = models.FloatField(null=True, blank=True)
    air_pressure = models.IntegerField(null=True, blank=True)
    air_humidity = models.IntegerField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_dir = models.CharField(null=True, blank=True)
    uv_index = models.FloatField(null=True, blank=True)
    moon_phase = models.CharField(null=True, blank=True)
    moon_illumination = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    bait = models.ForeignKey(Bait, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    fisherman = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Fishes'

    def __str__(self):
        return f"{self.species} at {self.timestamp}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.timestamp:%Y-%m-%d_%H-%M}")
        super().save(*args, **kwargs)
