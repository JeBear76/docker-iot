import asyncio
import json
import websockets

class socketServer:
    def __init__(self, actionObserver):
        self.connected = list()
        self.actionObserver = actionObserver

    def broadcast(self, message):
        print(f'Connected: {len(self.connected)}')
        for conn in self.connected:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                asyncio.run(conn.send(message))
            else:
                loop.run_until_complete(conn.send(message))

    async def handler(self, websocket, path):
        if websocket not in self.connected:
            self.connected.append(websocket)
        while True:
            try:
                data = await websocket.recv()
            except websockets.ConnectionClosedOK:
                self.connected.remove(websocket)
                print("Connection closed")
            print(data)
            reply = f"{data}"

            try:
                json_data = json.loads(data)
                # Data is in JSON format
                # Process the JSON data here
                if 'op' in json_data:
                    if self.actionObserver is not None:
                        self.actionObserver.sendAction(data)                    
                    reply = f"Sent message to topic 'docker-iot-thing-outtopic': {data}"
                if 'askOllama' in json_data:
                    if self.actionObserver is not None:
                        reply = self.actionObserver.askOllama(json_data['askOllama'])
                        await conn.send(f"Ollama: {reply}")
                        return
                    else:
                        reply = "Ollama is not available"

            except json.JSONDecodeError:
                pass
                # Data is not in JSON format
                # Handle the non-JSON data here
            print(reply)
            for conn in self.connected:
                try:
                    if conn == websocket:
                        await conn.send(f"Me: {reply}")
                        continue
                    await conn.send(reply)
                except websockets.exceptions.ConnectionClosedError:
                    pass

    async def webSocketMain(self):
        async with websockets.serve(self.handler, "0.0.0.0", 8000):
            await asyncio.Future()
