from sqlalchemy import func
from typing import Optional

#______________Import Dependencies___________________

from .Rep import Rep
from Py_Models.Tasks import Py_Tasks
from Models.Models import Task

class Tasks_Rep(Rep):

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self
    
    def __exit__(self,tb,val,ke):
        self.db.close()
    
    #______________Add new User___________________

    def Add_Task(self, task : Py_Tasks) -> Optional[Task]:
        task_obj = Task(** task.model_dump(exclude=['cretaed_by_userName', 'updated_by_userName']))
        try:
            self.db.add(task_obj)
            self.db.commit()
            self.db.refresh(task_obj)
            return task_obj
        except Exception as e:
            print(e)
            return None
        
    #______________Authentication_________________

    def Update_Task(self, task : Py_Tasks) -> int:
        try:
            temp_task = self.db.query(Task).filter(Task.id == task.id).first()
            temp_task.description = task.description
            temp_task.updated_at = task.updated_at
            temp_task.updated_by = task.updated_by
            temp_task.status = task.status
            temp_task.data = task.data

            self.db.commit()
            return 1
        except Exception as e:
            return -1
