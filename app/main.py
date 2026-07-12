from app import config
from fastapi import FastAPI
from app.routes import nutricion, payments, entrenamiento, videos
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from .auth import router as auth_router
import stripe
import os
from dotenv import load_dotenv
from app.routes import entrenamiento_historico
from app.routes import pesajes_historico
from app.routes import upfiles
from app.routes import chat
from app.routes import anamnesis

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
for env_name in ("FRONTEND_URL", "FRONTEND_URL_WWW"):
    url = os.getenv(env_name)
    if url and url not in origins:
        origins.append(url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(entrenamiento.router,
                   prefix="/entrenamiento", tags=["entrenamiento"])
app.include_router(entrenamiento_historico.router)
app.include_router(videos.router)
app.include_router(pesajes_historico.router)
app.include_router(upfiles.router)
app.include_router(chat.router)
app.include_router(anamnesis.router)


register_tortoise(
    app,
    db_url=os.getenv("db_url"),
    modules={"models": ["app.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

app.include_router(nutricion.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
