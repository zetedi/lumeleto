from fastapi import FastAPI
from database import engine, Base
from models import Lifeseed

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Lumeleto is growing 🌿"}