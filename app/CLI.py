import argparse
import requests

# Define the URLs for the two server instances
SERVER1_URL = "http://localhost:8000"
SERVER2_URL = "http://localhost:8001"

# Endpoints for controlling the game
START_ENDPOINT = "/start"
PAUSE_ENDPOINT = "/pause"
RESUME_ENDPOINT = "/resume"
STOP_ENDPOINT = "/stop"

def send_command(url, endpoint, params=None):
    try:
        if params:
            response = requests.get(f"{url}{endpoint}", params=params)
        else:
            response = requests.get(f"{url}{endpoint}")
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def start_game(pong_time_ms):
    params = {"pong_time_ms": pong_time_ms}
    send_command(SERVER1_URL, START_ENDPOINT, params)
    send_command(SERVER2_URL, START_ENDPOINT, params)

def pause_game():
    send_command(SERVER1_URL, PAUSE_ENDPOINT)
    send_command(SERVER2_URL, PAUSE_ENDPOINT)

def resume_game():
    send_command(SERVER1_URL, RESUME_ENDPOINT)
    send_command(SERVER2_URL, RESUME_ENDPOINT)

def stop_game():
    send_command(SERVER1_URL, STOP_ENDPOINT)
    send_command(SERVER2_URL, STOP_ENDPOINT)

def main():
    parser = argparse.ArgumentParser(description="Control the Pong game")
    parser.add_argument("command", type=str, choices=["start", "pause", "resume", "stop"], help="Command to execute")
    parser.add_argument("param", type=int, nargs='?', help="Parameter for the command")

    args = parser.parse_args()

    if args.command == "start":
        if args.param is None:
            print("Error: 'start' command requires 'pong_time_ms' parameter")
            return
        start_game(args.param)
    elif args.command == "pause":
        pause_game()
    elif args.command == "resume":
        resume_game()
    elif args.command == "stop":
        stop_game()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
