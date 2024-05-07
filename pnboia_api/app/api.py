from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from pnboia_api.app.v1 import auth, moored, drift, qualified_data, quality_control, metadata


app = FastAPI(title="PNBOIA API", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/test")
async def root():
    return {"Nginx": "I'm alive"}

#######################
# V1
#######################

app.include_router(moored.router, prefix="/moored", tags=["moored"])
app.include_router(drift.router, prefix="/drift", tags=["drift"])
app.include_router(qualified_data.router, prefix="/qualified_data", tags=["qualified_data"])
app.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
app.include_router(quality_control.router, prefix="/quality_control", tags=["quality_control"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

#######################
# V2
#######################
