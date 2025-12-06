from pydantic import BaseModel , ConfigDict , Field
from typing import Dict, List
from datetime import datetime

class Py_Boards(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True) # allow using arbitary fields like DateTime
    id: int | None = None
    title: str # Board title
    created_by: int 
    creation_date : datetime = Field(default_factory = datetime.now) # User's Registeration Date
    fields_list: List[Dict[str, str]] = Field(default_factory=list)
