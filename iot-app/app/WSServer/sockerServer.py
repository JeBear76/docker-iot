import asyncio
import json
import websockets

class socketServer:
    def __init__(self, actionObserver):
        self.connected = list()
        self.actionObserver = actionObserver

    async def sendSingleMessage(self, conn, message):
        try:
            await conn.send(message)
        except websockets.exceptions.ConnectionClosedError:
            self.connected.remove(conn)
        except websockets.exceptions.ConnectionClosedOK:
            self.connected.remove(conn)

    async def broadcast(self, message, websocket = None):
        print(f'Connected: {len(self.connected)}')
        for conn in self.connected:
            messageToSend = message
            if websocket is not None and conn == websocket:
                messageToSend = f"You: {message}"                
            await self.sendSingleMessage(conn, messageToSend)

    async def handler(self, websocket, path):        
        if websocket not in self.connected:
            self.connected.append(websocket)
        while True:
            try:
                data = await websocket.recv()
            except websockets.ConnectionClosedOK:
                self.connected.remove(websocket)
                print("Connection closed")
            if data is None:
                continue
            print(f"Received: {data}")
            reply = f"{data}"
            if await self.processJsonCommand(data, websocket):
                continue
            print(reply)
            await self.broadcast(reply, websocket)

    async def processJsonCommand(self, data, websocket):
        try:
            json_data = json.loads(data)
            if 'op' in json_data:
                if self.actionObserver is not None:
                    self.actionObserver.sendAction(data)                    
                reply = f"Sent message to topic 'docker-iot-thing-outtopic': {data}"
            else:
                if 'askOllama' in json_data:
                    if self.actionObserver is not None:
                        reply = self.actionObserver.askOllama(json_data['askOllama'])
                        reply = f"Ollama: {reply}"
                    else:
                        reply = "Ollama is not available"
                    print(reply)
                    await self.sendSingleMessage(websocket,reply)
        except json.JSONDecodeError:
            return False
        return True
    
    async def webSocketMain(self):
        async with websockets.serve(self.handler, "0.0.0.0", 8000):
            await asyncio.Future()
