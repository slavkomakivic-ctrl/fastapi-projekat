from fastapi import FastAPI
import database  # pokreće CREATE TABLE kad se importuje
from routes import router

app = FastAPI()
app.include_router(router)