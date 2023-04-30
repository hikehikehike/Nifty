from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from pathlib import Path

from chatbot import load_embeddings, get_response

app = FastAPI()

docsearch, chain = load_embeddings()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()

        response = get_response(message, docsearch, chain)

        await websocket.send_text(response)


@app.get("/")
async def get():
    file_path = Path("templates/index.html")
    return FileResponse(file_path)
