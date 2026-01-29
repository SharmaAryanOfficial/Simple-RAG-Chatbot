from fastapi import FastAPI
import uvicorn  
from src.routes.route import router
from contextlib import asynccontextmanager

from src.services.database_service import db_manager

from src.routes.route import router
from dotenv import load_dotenv
import os

load_dotenv(override=True)

@asynccontextmanager
async def lifespan(app : FastAPI):
    db_manager.initialize(Connection_string=os.getenv("DB_URI"))
    print("Database initialized")

    yield

    db_manager.close()
    print('Database connections closed')



app = FastAPI(lifespan=lifespan)

@app.get("/chat/threads")
def get_threads():
    return {"threads": []}  # start simple

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port = 8000)