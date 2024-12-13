import asyncio
import websockets
import json

connected_users = set()

async def websocket_handler(websocket, path):
    username = None
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data["command"] == "join_room":
                username = data["username"]
                connected_users.add(websocket)
                await broadcast(f"{username} has joined the chat!")

            elif data["command"] == "send_msg":
                msg = f"{username}: {data['message']}"
                await broadcast(msg)

            elif data["command"] == "leave_room":
                await websocket.close()
    except websockets.ConnectionClosed:
        print(f"Connection with {username} closed.")
        pass
    finally:
        if websocket in connected_users:
            connected_users.remove(websocket)
            if username:
                await broadcast(f"{username} has left the chat.")

async def broadcast(message):
    for user in connected_users:
        try:
            await user.send(message)
        except websockets.ConnectionClosed:
            pass

async def websocket_handler(websocket, path):
    # Handle incoming WebSocket connections
    print("New WebSocket connection")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

def start_websocket_server():
    port = 6800

    async def run_server():
        print(f"Starting WebSocket server on port {port}")
        async with websockets.serve(websocket_handler, "0.0.0.0", port):
            await asyncio.Future()  # Run forever

    # Create and run the event loop
    try:
        asyncio.run(run_server())
    except OSError as e:
        if e.errno == 98:  # Port already in use
            print(f"Port {port} is already in use. Please ensure no other instances are running.")
        else:
            print(f"An error occurred: {e}")
