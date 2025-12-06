import asyncio
from fastapi import APIRouter, Body, Query
from typing import Annotated

from Py_Models.Tasks import Py_Tasks
from Py_Models.Boards import Py_Boards
from Repository.Boards_Rep import Boards_Rep
from Repository.Tasks_Rep import Tasks_Rep
from Data_Layer.Redis_DB import RealTimeList
from Utilities.WebSocketClass import WebSocketManager

boards_route = APIRouter(prefix='/api/Boards') # basic router object

RedisDB = RealTimeList() # instanciate a new object from Redis Database as a Real-Time Database
ws_manager = WebSocketManager() # instanciate a new object from websocket manager class to send/receive tasks
streamer_task = None # main streamer

#________________Show Available Boards__________________

@boards_route.get('/All_Boards')
def Get_Boards():
    with Boards_Rep() as boards_rep:
        boards = boards_rep.All_Boards()
    return boards

#____________________Add new Board_______________________

@boards_route.post('/Add_Board')
async def Add_Boards(board : Py_Boards):
    with Boards_Rep() as boards_rep:
        result = boards_rep.Add_Board(board)
    
    if result != None: # board has been added to DataBase currectly
        global streamer_task
        streamer_task = asyncio.create_task(RedisDB.Streamer(result.id, ws_manager)) # create a new streamer with group consumer for created board
    
    return result.id

#____________________Add new Task________________________

@boards_route.post("/Tasks/Add")
async def add_Task(task : Annotated[Py_Tasks , Body()]):
    await RedisDB.add_Task(task = task , board_id = task.board_id)
    with Tasks_Rep() as task_rep: # add to database
        task_rep.Add_Task(task)

#____________________Update Tasks________________________

@boards_route.post("/Tasks/Update")
async def add_Task(task : Annotated[Py_Tasks , Body()]):
    await RedisDB.update_Task(task , board_id = task.board_id)
    with Tasks_Rep() as task_rep: # update database
        task_rep.Update_Task(task)

#____________________Tasks History________________________

@boards_route.get("/Tasks/History")
async def add_Task(task_id : Annotated[int , Query()], board_id : Annotated[int , Query()]):
    history = await RedisDB.get_task_history(board_id , task_id)
    return history