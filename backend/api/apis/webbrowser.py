from fastapi import APIRouter,Depends,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request

from api.prisma import prisma
import orbitpredictor as op
from typing import Optional
from groundstation import GroundStation
from geopy.geocoders import Nominatim 
import geocoder
from jinja2 import Environment, FileSystemLoader

router = APIRouter()
geocoder = Nominatim(user_agent = "backend")

templates = Jinja2Templates(directory="api/apis/templates")

@router.get("/{city}/{satellite}", response_class= HTMLResponse)
async def get_visibility(request:Request, city:str, satellite:str,interval: Optional[int] = 2*86400, elevation: Optional[int] = 15, height: Optional[int] = 2):
    g = geocoder.geocode(city)
    GS = GroundStation(city, g.latitude, g.longitude, height)

    sat = await prisma.satellite.find_first(
        where={
            'name': satellite,
        }
    )
    passes = op.predict_next_visible_orbits(sat.name, GS.observer, interval, None, elevation)
    
    
    context = {
        "visibilitywindows": passes,
        "satellite_name": satellite,
        #"satellite_id": sat.id,
        "Ground Station": GS,

    }


    #return passes
    return templates.TemplateResponse("visibilitywindow.html", {"request":request,"passes": passes, "satellite_name": satellite, "city":city})


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
