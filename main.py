# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.exceptions_handlers import register_exception_handlers
from api.router import api_router
from db.init_db import init_db
from logger.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="ToDo API")
app.mount("/home", StaticFiles(directory="home", html=True), name="home")
app.include_router(api_router)
register_exception_handlers(app)

logger.info("ToDo API запущен.")
for r in app.routes:
    methods = getattr(r, "methods", None)
    print("ROUTE:", r.path, methods)
