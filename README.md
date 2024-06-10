
# Pong Game Server

This project implements a simple Pong game using two FastAPI servers that ping-pong requests to each other. The game can be controlled using a CLI tool to start, pause, resume, and stop the game.

--------

## To get startede
Clone the repository:

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Requests

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/pong-game-server.git
   cd pong-game-server```
   
2. **Running the Servers**:

  Start Server 1:  
   ```sh
  python -m app.server server1
  ```

  Start Server 2:
   ```sh
  python -m app.server server2
  ```

3. **Using the CLI Tool**:

  Navigate to the app directory:
   ```sh
  cd app
  ```

  Start the game:
   ```sh
  python -m app.CLI start 1000
  ```

  Pause the game:
   ```sh
  python -m app.CLI pause
  ```

  Resume the game:
   ```sh
  python -m app.CLI resume
  ```

  Stop the game:
   ```sh
  python -m app.CLI stop
  ```
