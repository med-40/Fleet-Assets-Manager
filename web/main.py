from fastapi import FastAPI


app = FastAPI(
    title="Fleet Assets Manager",
    description="نظام تسيير الحضيرة",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Fleet-Assets-Manager Web Server يعمل بنجاح"
    }
