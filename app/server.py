from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import time
from threading import Thread
import uvicorn
import argparse
from app.state import state, pause_event, stop_event

app = FastAPI()

class StartRequest(BaseModel):
    pong_time_ms: int

TARGET_SERVER_URL = None

@app.get("/ping")
async def ping():
    if state.running and not state.paused:
        time.sleep(state.pong_time_ms / 1000.0)
        Thread(target = initial_ping).start()
    return "pong"
    raise HTTPException(status_code=503, detail="Server not ready")

@app.get("/start")
async def start_game(pong_time_ms: int):
    if state.running:
        return {"message": "Game already running"}
    state.running = True
    state.paused = False
    state.pong_time_ms = pong_time_ms
    stop_event.clear()
    pause_event.clear()
    Thread(target=initial_ping).start()
    return {"message": "Game started"}

@app.get("/pause")
async def pause_game():
    if not state.running:
        return {"message": "Game not running"}
    state.paused = True
    pause_event.set()
    return {"message": "Game paused"}

@app.get("/resume")
async def resume_game():
    if not state.running:
        return {"message": "Game not running"}
    elif not state.paused:
        return {"message": "Game is running but not paused"}
    state.paused = False
    pause_event.clear()
    return {"message": "Game resumed"}

@app.get("/stop")
async def stop_game():
    if not state.running:
        return {"message": "Game not running"}
    state.running = False
    stop_event.set()
    return {"message": "Game stopped"}

def initial_ping():
    if not state.paused:
        try:
            response = requests.get(TARGET_SERVER_URL)
            if response.status_code == 200:
                print(f"Received pong from {TARGET_SERVER_URL}")
        except requests.RequestException as e:
            print(f"Error sending ping to {TARGET_SERVER_URL}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a Pong server instance")
    parser.add_argument("instance", type=str, choices=["server1", "server2"], help="Server instance to start (server1 or server2)")
    args = parser.parse_args()

    if args.instance == "server1":
        TARGET_SERVER_URL = "http://localhost:8001/ping"
        uvicorn.run(app, host="0.0.0.0", port=8000)
    elif args.instance == "server2":
        TARGET_SERVER_URL = "http://localhost:8000/ping"
        uvicorn.run(app, host="0.0.0.0", port=8001)
