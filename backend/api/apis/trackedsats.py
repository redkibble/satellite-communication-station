from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from api.prisma import prisma
import orbitpredictor as op
from groundstation import GroundStation
router = APIRouter()
