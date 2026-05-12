from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Server received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# Serve client.html at "/"
@app.get("/")
async def get():
    return FileResponse("client.html")
