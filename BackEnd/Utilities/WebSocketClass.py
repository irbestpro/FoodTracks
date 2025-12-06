from typing import Dict, List
from fastapi import WebSocket

class WebSocketManager:
    
    #___________Create a list of active connected Users_______________

    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {} # create an empty object from list of websockets

    #______________Handle Connect Method to Connect Users_____________

    async def connect(self, board_id: int, websocket: WebSocket):
        await websocket.accept() # accept user request
        if board_id not in self.active_connections: # prevent duplication in user connection
            self.active_connections[board_id] = []
        self.active_connections[board_id].append(websocket)

    #__________________Handle Disconnect Method_______________________

    async def disconnect(self, board_id: int, websocket: WebSocket):
        self.active_connections[board_id].remove(websocket)

    #_____________________Broad Cast a Message_________________________

    async def broadcast(self, board_id: int, message: dict):
        board_id = int(board_id)
        if board_id in self.active_connections:
            dead = [] # disconnected Users (Broken Connections)
            for ws in self.active_connections[board_id]:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    dead.append(ws)
            
            #_____________Disconnected Users__________________
            
            for ws in dead:
                await self.disconnect(board_id, ws)
