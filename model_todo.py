from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str
    title: str
    desc: str
    checked: bool