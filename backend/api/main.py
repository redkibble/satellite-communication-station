"""Main FastAPI app instance declaration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.apis import apis
from api.prisma import prisma

app = FastAPI(
    title="Ground Station API",
    openapi_url="/openapi.json",
    docs_url="/",
)
app.include_router(apis)

origins = ['*'
    #"",
    #"http://localhost:3000",
    #"http://localhost",
    #"http://localhost:8080",
]

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in origins], # changed [] to origins and referring to the list above
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await prisma.connect()
@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
@app.get("/")
def read_root():
    return {"version": "1.0.0"}

# Guards against HTTP Host Header attacks
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"])
