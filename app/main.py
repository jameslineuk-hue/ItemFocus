from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import tags

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"

app = FastAPI(title="ItemFocus", description="Tagged items QR finder")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(tags.router, prefix="/api")


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
