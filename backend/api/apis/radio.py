from fastapi import APIRouter, Depends, HTTPException
from api.prisma import prisma
import orbitpredictor as op
from pydantic import BaseModel


router = APIRouter()
class Radio(BaseModel):
    name: str
    rtype: str
    port: str

@router.get("/")
async def get_radios():
    radios = await prisma.radio.find_many()
    return {"status": "ok", "result": radios}

@router.get("/{radio_id}")
async def get_radio(radio_id: int):
    radio = await prisma.radio.find_first(
        where={
            'id': radio_id
        }
    )
    # Check radios connection status and send back status code.
    return {
        "status": "ok",
        "result": radio
    }


@router.post("/")
async def create_radio(radio: Radio):
    newradio = await prisma.radio.create(data=radio.dict())
    return newradio