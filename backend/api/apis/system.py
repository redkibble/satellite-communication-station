from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import orbitpredictor as op
from api.prisma import prisma
router = APIRouter()

@router.get('/status')
async def status():
    gs = await prisma.groundstation.count()
    result = {
        "stations": gs,
        "uptime": 0,
    }
    return {"status": "ok", "result": result}

@router.get('/tle/refresh')
async def refresh_tle():
    await op.refresh_tles()
    return {"status": "ok"}
    