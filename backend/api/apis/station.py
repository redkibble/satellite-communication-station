from fastapi import APIRouter, Depends, HTTPException
from api.prisma import prisma
import orbitpredictor as op
from groundstation import GroundStation
from pydantic import BaseModel
router = APIRouter()

class Groundstation(BaseModel):
    name: str
    latitude: float
    longitude: float
    height: float

@router.get("/")
async def get_station():
    gss = await prisma.groundstation.find_many()
    return gss


@router.post("/")
async def create_station(gs: Groundstation):
    newgs = await prisma.groundstation.create(data=gs.dict())
    return newgs


