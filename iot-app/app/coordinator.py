import asyncio
import IoTMqtt.iot as iot
import WSServer.sockerServer as socketServer

class coordinator:
    def __init__(self):
        self.iotConnection = iot.iot(self)
        self.websocket = socketServer.socketServer(self)        

    def sendAction(self, data):
        self.iotConnection.send_message('docker-iot-thing-outtopic', data)

    def broadcast(self, data):
        self.websocket.broadcast(data)     
    
    def run(self):
        self.iotConnection.connectAdSubscribe()        
        asyncio.run(self.websocket.webSocketMain())
        