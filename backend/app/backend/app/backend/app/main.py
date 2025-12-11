import uvicorn
from fastapi import FastAPI
from .config import settings
from .db import init_db
from .routers import auth, wallet, services

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Register routers
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(services.router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to ALFA by Daral Travel API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
