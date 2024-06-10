from pydantic import BaseModel
from threading import Event

class GameState(BaseModel):
    running: bool = False
    paused: bool = False
    pong_time_ms: int = 1000

# Shared state instance
state = GameState()

# Events to control the game loop
pause_event = Event()
stop_event = Event()
