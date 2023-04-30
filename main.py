import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from pathlib import Path

from chatbot import load_embeddings, get_response
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException

app = FastAPI()

docsearch, chain = load_embeddings()
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(name="X-API-KEY")


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=400, detail="Invalid API Key")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that listens to incoming messages and sends a response back.
    """
    await websocket.accept()
    while True:
        message = await websocket.receive_text()

        response = get_response(message, docsearch, chain)

        await websocket.send_text(response)


@app.get("/", dependencies=[Depends(get_api_key)])
async def get():
    """
    GET endpoint that serves the index.html file.
    """
    file_path = Path("templates/index.html")
    return FileResponse(file_path)
