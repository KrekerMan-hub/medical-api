#==========================
# FastAPI
#==========================

from fastapi import FastAPI
from database import init_db
from routers.patients import router as patients_router

init_db()

app = FastAPI(title="Medical API", version="1.0")
app.include_router(patients_router)

@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Мой первый API работает!"}

@app.get("/about")
def about():
    return {
        "project": "Medical API",
        "author": "Тарас"
    }  