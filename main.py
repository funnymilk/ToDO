# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import api_router
from db.init_db import init_db

init_db() 
app = FastAPI(title="ToDo API")
app.mount("/home", StaticFiles(directory="home", html=True), name="home")
app.include_router(api_router)
