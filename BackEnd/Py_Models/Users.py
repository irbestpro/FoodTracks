from pydantic import BaseModel , ConfigDict , Field
from datetime import datetime

class Py_Users(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True) # allow using arbitary fields like DateTime
    id: int | None = None
    name: str # User's FullName
    username: str 
    email: str
    password: str
    creation_date : datetime = Field(default_factory = datetime.now) # User's Registeration Date
