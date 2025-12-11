import uvicorn
from fastapi import FastAPI
from .config import settings
from .db import init_db
from .routers import auth, services

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(auth.router)
app.include_router(services.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
