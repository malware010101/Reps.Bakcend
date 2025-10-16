from fastapi import FastAPI
from app.routes import nutricion, payments, entrenamiento
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from .auth import router as auth_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

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


register_tortoise(
    app,
    db_url="sqlite://nutri_and_entrena.sqlite",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(nutricion.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
