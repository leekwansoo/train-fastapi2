from pydantic import BaseModel

class Train(BaseModel): 
    name: str
    pushup: int    
    stomach: int
    squat: int
    arm: int
    uplift: int
    upheel: int