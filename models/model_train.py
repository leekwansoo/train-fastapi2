from typing import Optional
from pydantic import BaseModel, Field

class Train(BaseModel):
    date: Optional[str] = None
    user: Optional[str] = None
    pushup: Optional[int] = None
    stomach: Optional[int] = None
    squat: Optional[int] = None
    arm: Optional[int] = None
    uplift: Optional[int] = None
    upheel: Optional[int] = None
    kick_on_chair: Optional[int] = None
    spreading_thigh: Optional[int] = None
    id: Optional[str] = None

class FormData(BaseModel):
    date: Optional[str] = None
    user: Optional[str] = None
    pushup: Optional[int] = None
    stomach: Optional[int] = None
    squat: Optional[int] = None
    arm: Optional[int] = None
    uplift: Optional[int] = None
    upheel: Optional[int] = None
    kick_on_chair: Optional[int] = None
    spreading_thigh: Optional[int] = None

