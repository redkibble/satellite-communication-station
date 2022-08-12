from curses import baudrate
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from api.prisma import prisma
import orbitpredictor as op
from groundstation import GroundStation

router = APIRouter()

@router.get("/")
async def get_radios():
    return []

@router.get("/{radio_id}")
async def get_radio(radio_id: int):
    return {
        "baudrate": 3600
    }