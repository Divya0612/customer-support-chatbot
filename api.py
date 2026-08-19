from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app import get_response

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="frontend")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def index():
    return FileResponse("frontend/index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    response = get_response(request.message)
    return {"response": response}
