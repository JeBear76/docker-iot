import asyncio
import IoTMqtt.iot as iot
import WSServer.sockerServer as socketServer
import OllamaConnector.ollamaConnector as ollamaConnector
import os

class coordinator:
    def __init__(self):
        _ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.iotConnection = iot.iot(self)
        self.websocket = socketServer.socketServer(self) 
        self.ollamaChat = ollamaConnector.ollamaConnector(_ollama_url)       

    def sendAction(self, data):
        self.iotConnection.send_message('docker-iot-thing-outtopic', data)

    def askOllama(self, text):
        return self.ollamaChat.getResponse(text)
    
    def broadcast(self, data):
        self.websocket.broadcast(data)     
    
    def run(self):
        self.iotConnection.connectAdSubscribe()        
        asyncio.run(self.websocket.webSocketMain())
        