from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import SessionLocal


app = FastAPI(
    title="Fleet Assets Manager",
    description="نظام تسيير الحضيرة",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "application": "Fleet Assets Manager",
        "status": "running",
        "message": "نظام تسيير الحضيرة يعمل بنجاح"
    }


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
