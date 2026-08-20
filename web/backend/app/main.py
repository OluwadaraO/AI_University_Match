from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base
from app.models.student import Student

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI University Match For Students"}
