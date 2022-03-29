from threading import current_thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import queue


class Payload(BaseModel):
    id: str
    img: str
    type: int
    misc: Optional[list] = []


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logs = queue.Queue()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/log", tags=["logs"])
async def get_log() -> dict:
    if logs.empty():
        current_log = {}
    else:
        current_log = logs.get()
    return current_log


@app.post("/log", tags=["logs"])
async def post_log(log: Payload) -> dict:
    logs.put(log)
    return {
        "data": {"log successfully posted."}
    }
