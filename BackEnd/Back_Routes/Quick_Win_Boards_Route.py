import asyncio
from fastapi import APIRouter, Body, Query
from typing import Annotated

from Py_Models.Boards import Py_Boards
from Py_Models.Tasks import Py_Tasks
from Data_Layer.Quick_Win import RealTimeListInMemory
from Utilities.WebSocketClass import WebSocketManager

qw_boards_route = APIRouter(prefix='/api/qw/Boards')

MemoryDB = RealTimeListInMemory()  
ws_manager = WebSocketManager()    
streamer_tasks = {}                
boards_memory = {}  # In-Memory DataBase

#________________Show Available Boards__________________

@qw_boards_route.get('/All_Boards')
def Get_Boards():
    return list(boards_memory.values())

#____________________Add new Board______________________

@qw_boards_route.post('/Add_Board')
async def Add_Boards(board: Py_Boards):
    # Generate a simple unique ID
    board_id = id(board)
    boards_memory[board_id] = {"id": board_id, "name": board.name}

    # Start streamer for this board if not already running
    if board_id not in streamer_tasks:
        streamer_tasks[board_id] = asyncio.create_task(MemoryDB.Streamer(board_id, ws_manager))

    return board_id

#____________________Add new Task________________________

@qw_boards_route.post("/Tasks/Add")
async def add_Task(task: Annotated[Py_Tasks, Body()]):
    added_task = await MemoryDB.add_Task(task=task, board_id=task.board_id)
    return added_task

#____________________Update Tasks________________________

@qw_boards_route.post("/Tasks/Update")
async def update_Task(task: Annotated[Py_Tasks, Body()]):
    updated_task = await MemoryDB.update_Task(task, board_id=task.board_id)
    return updated_task

# _____________________Get All Tasks_____________________

@qw_boards_route.get("/Tasks/{board_id}")
async def get_all_tasks(board_id: int):
    tasks = await MemoryDB.all_tasks(board_id)
    return tasks

@qw_boards_route.get("/Tasks/History")
async def add_Task(task_id : Annotated[int , Query()], board_id : Annotated[int , Query()]):
    history = await MemoryDB.get_task_history(board_id , task_id)
    return history
