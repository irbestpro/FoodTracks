import asyncio
from datetime import datetime
from typing import Optional, Dict, List
from Py_Models.Tasks import Py_Tasks
from Utilities.WebSocketClass import WebSocketManager

class RealTimeListInMemory:
    _board_name = "board"

    #_________________Initialization__________________

    def __init__(self):
        self.boards: Dict[int, Dict[int, dict]] = {}
        self.counters: Dict[int, int] = {}
        self.streams: Dict[int, List[dict]] = {} # like Redis Streamer

    #_______________Add new Task To list________________

    async def add_Task(self, task: Py_Tasks, board_id: int) -> Py_Tasks:
        try:
           
            if board_id not in self.boards: # generate new board in memory
                self.boards[board_id] = {}
                self.counters[board_id] = 0
                self.streams[board_id] = []

            self.counters[board_id] += 1 # generate new task_id
            task.id = self.counters[board_id]
            self.boards[board_id][task.id] = task.model_dump() # save the task

            event = {"action": "Add", "task": task.model_dump(), "timestamp": datetime.utcnow().isoformat()} # add new event
            self.streams[board_id].append(event) # save in stream
            return task
        
        except Exception as e:
            print(f"Error adding task: {e}")
            return None

    #__________Update Existing Tasks in list____________

    async def update_Task(self, task: Py_Tasks, board_id: int) -> Optional[Py_Tasks]:
        try:
            board = self.boards.get(board_id)
            if not board or task.id not in board:
                return None

            if board[task.id].get("status") == "finished":
                return None
            board[task.id] = task.model_dump() # update tasks

            event = {"action": "Update", "task": task.model_dump(), "timestamp": datetime.utcnow().isoformat()} # add new event
            self.streams[board_id].append(event) # update in-memory streamer
            return task
        
        except Exception as e:
            print(f"Error updating task: {e}")
            return None

    #______________Remove a Task From List_________________

    async def remove_task(self, board_id: int, task_id: int) -> int:
        try:
            board = self.boards.get(board_id)
            if not board or task_id not in board:
                return -1
            
            del board[task_id] # remove task

            event = {"action": "Delete", "task_id": task_id, "timestamp": datetime.utcnow().isoformat()} # add new event
            self.streams[board_id].append(event) # add new event in streamer class
            return task_id
        
        except Exception as e:
            print(f"Error removing task: {e}")
            return -1
        
    #__________Get the history of specific task____________

    async def get_task_history(self, board_id: int, task_id: int) -> list[dict]:
        history = []
        events = self.streams.get(board_id, []) # get events from in-memory stream

        for event in events:
            action = event.get("action")
            data = event.get("task") or event.get("task_id")

            if isinstance(data, dict): # added/modified tasks
                tid = data.get("id")
            else:
                tid = int(data) # removed Tasks

            if (action in ["Add", "Update"] and tid == task_id) or (action == "Delete" and tid == task_id): # just Events of individual task
                history.append(event)

        return history

    #_________________Return all tasks___________________

    async def all_tasks(self, board_id: int) -> List[dict]:
        board = self.boards.get(board_id, {}) # get all tasks
        tasks = list(board.values()) # get individual task
        tasks.sort(key=lambda x: x.get("updated_at", ""), reverse=False) # sort by update time
        tasks.sort(key=lambda x: x.get("status", ""), reverse=True) # sort by status
        return tasks

    #______________Redis Streamer and Websocket_________________

    async def Streamer(self, board_id: int, ws_manager: WebSocketManager):
        if board_id not in self.streams:
            self.streams[board_id] = []

        last_index = 0
        while True:
            try:
                events = self.streams[board_id][last_index:]
                if not events:
                    await asyncio.sleep(0.1)
                    continue

                for event in events:
                    await ws_manager.broadcast(board_id, event)
                    last_index += 1

                await asyncio.sleep(0.1)

            except Exception as e:
                print("Streamer error:", e)
                await asyncio.sleep(1)

    #__________Delete All the entries from Memory_____________

    async def reset_DB(self):
        self.boards.clear()
        self.counters.clear()
        self.streams.clear()
