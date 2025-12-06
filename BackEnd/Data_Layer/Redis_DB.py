import json
import asyncio
import redis.asyncio as redis
from typing import Optional
from datetime import datetime

#________Import Models and Websocket Interface_______

from Py_Models.Tasks import Py_Tasks
from Utilities.WebSocketClass import WebSocketManager

#__________Import Redis Structure Data________________

from Utilities.Redis_Config import Redis_Config

class RealTimeList:

    _board_name = "board"

    #_________________Initialization__________________

    def __init__(self):
        conf = Redis_Config()
        self.client = redis.Redis(host = conf.host, port = conf.port, db = conf.db, decode_responses = True, password = conf.password)

    #_______________Add new Task To list________________
    
    async def add_Task(self, task: Py_Tasks, board_id: int) -> Py_Tasks:
        try:
            new_id = await self.client.incr(f"{self._board_name}:{board_id}:counter") # count the number of tasks in each board
            task.id = new_id # update task_id (automatically)
            key = f"{self._board_name}:{board_id}:Task:{new_id}"
            await self.client.set(key, json.dumps(task.model_dump())) # save stringified json

            # Sorted set index
            date_score = datetime.fromisoformat(task.created_at).timestamp()
            await self.client.zadd(f"{self._board_name}:{board_id}:manipulation_time",{str(new_id): date_score}) # add new sortable list (index)

            # Add new stream event (event bus)
            await self.client.xadd(f"{self._board_name}:{board_id}:stream",
                                   {"action": "Add", "task": json.dumps(task.model_dump())})

            return task

        except Exception as e:
            print(f"An error has occurred during task add: {e}")
            return None
    
    #__________Update Existing Tasks in list____________

    async def update_Task(self, task: Py_Tasks, board_id: int) -> Optional[Py_Tasks]:
        try:
            key = f"{self._board_name}:{board_id}:Task:{task.id}"
            data = await self.client.get(key) # get data from redis-database

            if (json.loads(data).get("status") == 'finished'): # check if the target task is finished or not?
                return None

            await self.client.set(key, json.dumps(task.model_dump()))# update a task
            await self.client.zadd(f"{self._board_name}:{board_id}:manipulation_time",{str(task.id): datetime.utcnow().timestamp()}) # update index scores list

            # Stream event
            await self.client.xadd(f"{self._board_name}:{board_id}:stream",
                                   {"action": "Update", "task": json.dumps(task.model_dump())}
            ) # borad cast a message on the board's channel

            return task
        
        except Exception as e:
            print(f"An error has occurred during task update: {e}")
            return None
        
    #______________Remove a Task From List_________________
        
    async def remove_task(self, board_id: int, task_id: int) -> int:
        key = f"{self._board_name}:{board_id}:Task:{task_id}"
        del_result = await self.client.delete(key) # delete a task from list
        if not del_result:
            return -1

        await self.client.zrem(
            f"{self._board_name}:{board_id}:manipulation_time",
            str(task_id)
        ) # remove task from index list

        # Stream event
        await self.client.xadd(
            f"{self._board_name}:{board_id}:stream",
            {"action": "delete", "task_id": str(task_id)}
        ) # remove task from list

        return del_result
        
    #_________________Return all tasks___________________
    
    async def all_tasks(self, board_id: int) -> Optional[list[Py_Tasks]]:
        query = f"{self._board_name}:{board_id}:Task:*" # to return all tasks
        tasks = []

        async for key in self.client.scan_iter(query):
            data = await self.client.get(key)
            if data:
                tasks.append(Py_Tasks(**json.loads(data)).model_dump())

        tasks.sort(key=lambda x: x["updated_at"])
        tasks.sort(key=lambda x: x["status"], reverse=True)# sort keys
        
        return tasks
    
    #__________Get the history of specific task____________

    async def get_task_history(self, board_id: int, task_id: int) -> list[dict]:
        stream_key = f"{self._board_name}:{board_id}:stream"
        history = []

        events = await self.client.xrange(stream_key, min='-', max='+') # Read all stream entries from the beginning
        
        for event_id, fields in events:
            action = fields["action"]
            raw = fields.get("task") or fields.get("task_id")
            try:
                data = json.loads(raw)
            except:
                data = raw

            if (action in ["Add", "Update"] and data.get("id") == task_id) or (action == "delete" and int(data) == task_id):
                history.append({"event_id": event_id, "action": action, "data": data})

        return history
    
    #______________Redis Streamer and Websocket_________________

    async def Streamer(self, board_id: int, ws_manager: WebSocketManager):
        stream_key = f"{self._board_name}:{board_id}:stream"

        # Create a consumer group with redis streamer
        try:
            await self.client.xgroup_create(stream_key, "to_do_list", id="0", mkstream =True)
        except Exception:
            pass

        while True:
            try:
                events = await self.client.xreadgroup( # real-time event handler
                                            "to_do_list",
                                            "Consumer1", # for horizontal scaling, We can Add another servers 
                                            streams={stream_key: ">"},
                                            count = 50,
                                            block = 1000
                                        )

                if not events: # No event has found!
                    continue

                for _, entries in events:
                    for event_id, fields in entries:
                        action = fields["action"] # get the last actions
                        raw = fields.get("task") or fields.get("task_id") # get inserted/updated or removed tasks respectively

                        try:
                            data = json.loads(raw) # message's data
                        except:
                            data = raw # message status

                        message = {"event_id": event_id,"action": action,"data": data} # latest message in board

                        await ws_manager.broadcast(board_id, message) # borad cast message to all consumers in a group
                        await self.client.xack(stream_key, "to_do_list", event_id) # get acknowledge from consumer

            except Exception as e:
                print("Streamer error:", e)
                await asyncio.sleep(1) # wait a moment and try to connect and broadcast again
    
    #_____________Delete All the entries from DB_____________

    async def reset_DB(self):
        self.client.flushdb() # reset db
