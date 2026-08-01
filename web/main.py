from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import text

from app.database.session import SessionLocal


BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "templates" / "index.html"


app = FastAPI(
    title="Fleet Assets Manager",
    description="نظام تسيير الحضيرة",
    version="1.0.0"
)


@app.get("/")
def home():
    return FileResponse(INDEX_FILE)


@app.get("/health")
def health_check():

    db = None

    try:
        db = SessionLocal()

        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as error:

        return {
            "status": "error",
            "database": "disconnected",
            "message": str(error)
        }

    finally:

        if db is not None:
            db.close()
