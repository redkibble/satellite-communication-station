from fastapi import APIRouter,Depends,HTTPException
from api.prisma import prisma
import orbitpredictor as op
from typing import Optional
from groundstation import GroundStation
from geopy.geocoders import Nominatim 
import geocoder

router = APIRouter()
geocoder = Nominatim(user_agent = "backend")

@router.get("/{city}/{satellite}")
async def get_visibility(city:str, satellite:str,interval: Optional[int] = 2*86400, elevation: Optional[int] = 15, height: Optional[int] = 2):
    g = geocoder.geocode(city)
    GS = GroundStation(city, g.latitude, g.longitude, height)

    sat = await prisma.satellite.find_first(
        where={
            'name': satellite,
        }
    )
    passes = op.predict_next_visible_orbits(sat.name, GS.observer, interval, None, elevation)
    return passes


@router.get("/{city}/{minimum_angular_elevation}/{height}/{satellite}")
async def get_visibility(city:str, satellite:str,interval: Optional[int] = 2*86400, minimum_angular_elevation: Optional[int] = 15, height: Optional[int] = 2):
    g = geocoder.geocode(city)
    GS = GroundStation(city, g.latitude, g.longitude, height)

    sat = await prisma.satellite.find_first(
        where={
            'name': satellite,
        }
    )
    passes = op.predict_next_visible_orbits(sat.name, GS.observer, interval, None, minimum_angular_elevation)
    return passes

@router.get("/{city}/{minimum_angular_elevation}/{height}/{satellite}/{interval}")
async def get_visibility(city:str, satellite:str,interval: Optional[int] = 2*86400, minimum_angular_elevation: Optional[int] = 15, height: Optional[int] = 2):
    g = geocoder.geocode(city)
    GS = GroundStation(city, g.latitude, g.longitude, height)

    sat = await prisma.satellite.find_first(
        where={
            'name': satellite,
        }
    )
    passes = op.predict_next_visible_orbits(sat.name, GS.observer, interval, None, minimum_angular_elevation)
    return passes