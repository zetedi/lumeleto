from fastapi import FastAPI
from database import engine, Base
from models import Lifeseed
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("🚀 Starting up Lumeleto node...")
        # Create DB tables
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        logging.info("🌙 Shutting down Lumeleto node...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Lumeleto is growing 🌿"}