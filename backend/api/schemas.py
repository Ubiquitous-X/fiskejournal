from ninja import Schema
from datetime import datetime
from typing import Optional

# Schema för user data output
class UserOut(Schema):
    username: str

# Schema för fish species
class FishSpeciesOut(Schema):
    id: int
    name: str
    latin_name: str
    description: Optional[str] = None

class FishSpeciesCreate(Schema):
    name: str
    latin_name: str
    description: Optional[str] = None

# Schema för bait
class BaitOut(Schema):
    id: int
    type: str

class BaitCreate(Schema):
    type: str

# Base schema för fish data
class FishBase(Schema):
    medium_image_url: str
    thumbnail_image_url: str
    species: Optional[FishSpeciesOut] = None
    latitude: float
    longitude: float
    air_temperature: Optional[float] = None
    air_pressure: Optional[int] = None
    air_humidity: Optional[int] = None
    weather: Optional[str] = None
    weather_icon_url: Optional[str] = None
    wind_speed: Optional[float] = None
    wind_dir: Optional[str] = None
    uv_index: Optional[float] = None
    moon_phase: Optional[str] = None
    moon_illumination: Optional[float] = None
    weight: Optional[float] = None
    length: Optional[float] = None
    bait: Optional[BaitOut] = None
    location: Optional[str] = None
    description: Optional[str] = None

# Schema för skapande av ny fisk
class FishCreate(FishBase):
    timestamp: datetime

# Schema för att uppdatera en fisk
class FishUpdate(Schema):
    medium_image_url: Optional[str] = None
    thumbnail_image_url: Optional[str] = None
    species: Optional[int] = None  # Referens till FishSpecies ID
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    air_temperature: Optional[float] = None
    air_pressure: Optional[int] = None
    air_humidity: Optional[int] = None
    weather: Optional[str] = None
    weather_icon_url: Optional[str] = None
    wind_speed: Optional[float] = None
    wind_dir: Optional[str] = None
    uv_index: Optional[float] = None
    moon_phase: Optional[str] = None
    moon_illumination: Optional[float] = None
    weight: Optional[float] = None
    length: Optional[float] = None
    bait: Optional[int] = None  # Referens till Bait ID
    location: Optional[str] = None
    description: Optional[str] = None

# Schema för att hämta fish data med extra fält
class FishOut(FishBase):
    id: int
    timestamp: datetime
    fisherman: UserOut
    slug: str

    class Config:
        from_attributes = True
