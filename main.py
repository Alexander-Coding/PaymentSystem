import os
import sys

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded

from src.routers import all_routers
from src.db.models import *
from src.database import create_db


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=500)


app.state.limiter = limiter


for route in all_routers:
    app.include_router(route)


def custom_openapi():
    openapi_schema = get_openapi(
        title="BioSense API",
        version="0.0.1",
        description="API web-приложения BioSense",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/docs")
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/")
async def index():
    return RedirectResponse('/docs')


@app.exception_handler(RateLimitExceeded)
async def ratelimit_exception_handler():
    return JSONResponse(
        status_code=429,
        content={"detail": "Вы превысили лимит попыток. Попробуйте снова через минуту."},
    )


@app.on_event("startup")
async def startup():
    await create_db()


@app.on_event("shutdown")
async def shutdown():
    pass
