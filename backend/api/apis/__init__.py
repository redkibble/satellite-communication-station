from fastapi import APIRouter
from api.apis.satellite import router as satellite_router
from api.apis.station import router as station_router
from api.apis.trackedsats import router as trackedsats_router
from api.apis.radio import router as radio_router
from api.apis.system import router as system_router
from api.apis.webbrowser import router as webbrowser_router

apis = APIRouter()
apis.include_router(webbrowser_router, prefix= "/webbrowser")
apis.include_router(satellite_router, prefix="/api/satellite")
apis.include_router(station_router, prefix="/api/station")
apis.include_router(trackedsats_router, prefix="/api/trackedsats")
apis.include_router(radio_router, prefix="/api/radio")
apis.include_router(system_router, prefix="/api/system")

__all__ = ["apis"]
