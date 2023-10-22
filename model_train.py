from typing import Optional
from pydantic import BaseModel, Field

class Train(BaseModel):
    user: Optional[str] = None
    date: Optional[str] = None
    pushup: Optional[int] = None
    stomach: Optional[int] = None
    squat: Optional[int] = None
    arm: Optional[int] = None
    uplift: Optional[int] = None
    upheel: Optional[int] = None
    kick_on_chair: Optional[int] = None
    spreading_thigh: Optional[int] = None

class FormData(BaseModel):
    user: Optional[str] = None
    date: Optional[str] = None
    pushup: Optional[int] = None
    stomach: Optional[int] = None
    squat: Optional[int] = None
    arm: Optional[int] = None
    uplift: Optional[int] = None
    upheel: Optional[int] = None
    kick_on_chair: Optional[int] = None
    spreading_thigh: Optional[int] = None

    class Config:
        orm_mode = True