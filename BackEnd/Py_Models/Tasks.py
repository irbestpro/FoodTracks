from typing import Dict , Any
from pydantic import BaseModel , ConfigDict , Field
from datetime import datetime

class Py_Tasks(BaseModel):
    id: int | None = None
    description: str
    board_id: int
    created_by: int
    cretaed_by_userName: str | None = None
    updated_by_userName: str | None = None
    created_at: str | None = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str | None = Field(default_factory=lambda: datetime.now().isoformat())
    updated_by: int | None = None
    status: str  # Active/Disabled
    data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models