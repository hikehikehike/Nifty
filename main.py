from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from pathlib import Path

from chatbot import load_embeddings, get_response

app = FastAPI()

docsearch, chain = load_embeddings()


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


@app.get("/")
async def get():
    """
    GET endpoint that serves the index.html file.
    """
    file_path = Path("templates/index.html")
    return FileResponse(file_path)
