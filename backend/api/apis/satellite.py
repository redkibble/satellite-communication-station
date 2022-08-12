from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from api.prisma import prisma
import orbitpredictor as op
from groundstation import GroundStation
router = APIRouter()

router = APIRouter()

@router.get("/")
async def get_satellites():
    satellites = await prisma.satellite.find_many()
    return satellites

@router.get("/{satellite_id}")
async def get_satellite(satellite_id: int):
    satellite = await prisma.satellite.find_first(
        where={
            'id': satellite_id
        }
    )
    return satellite

@router.get("/{satellite_name}/passes")
async def get_satellite_passes(satellite_name: str, interval: Optional[int] = 86400):
    satellite = await prisma.satellite.find_first(
        where={
            'name': satellite_name,
        }
    )
    # TODO: Accept groundstation id in query param. 
    GS = await prisma.groundstation.find_first()
    GS = GroundStation(GS.name, GS.latitude, GS.longitude, GS.height)
    passes = op.predict_next_visible_orbits(satellite.name, GS.observer, interval)
    return passes
    # return passes

@router.get("/{satellite_name}/observe")
async def observe_satellite(satellite_name: str):
    satellite = await prisma.satellite.find_first(
        where={
            'name': satellite_name
        }
    )
    # TODO: Accept groundstation id in query param. 
    GS = await prisma.groundstation.find_first()
    GS = GroundStation(GS.name, GS.latitude, GS.longitude, GS.height)
    next_pass =  op.predict_sattelite(satellite.name, GS.observer)
    return {"sattelite": satellite, "next_pass": next_pass}


