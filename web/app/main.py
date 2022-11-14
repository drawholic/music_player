from fastapi import FastAPI
from .db.db import init_models
from .users.router import router as users_router

app = FastAPI()


app.include_router(users_router)


@app.on_event('startup')
async def startup():
    await init_models()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str = 'Vladick'):
    return {"message": f"Hello {name}"}
