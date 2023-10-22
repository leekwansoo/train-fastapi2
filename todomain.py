from fastapi import FastAPI, HTTPException, UploadFile, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, Response
from typing import Annotated
import uvicorn
from database import *
from database_user import *


origins = ["*"] 
# This will eventually be changed to only the origins you will use once it's deployed, to secure the app a bit more.

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# convert list into tuple
def convert_list_tuple(list):
    return tuple(list)

CHUNK_SIZE = 1024*1024

# Image List Table
headings = ("Image_Name", "Display", "Delete")
data = () 


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request} )

@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request} )
  
@app.post('/login', response_model=Login)
async def login_process(id: Annotated[str, Form()], pw: Annotated[str, Form()]):
    print(id, pw)
    result = await find_user(id)
    if not result: raise HTTPException(400)
    if not result.pw == pw: raise HTTPException(400)
    return ("login successful")

@app.post("/api/add-task", response_model=Task)
async def add_task(task: Task):
    result = await create_task(task)
    if not result: raise HTTPException(400)
    return result

@app.post('/register', response_model=Login)
async def user_register(id: Annotated[str, Form()], pw: Annotated[str, Form()]):
    user = {"id": id, "pw": pw}
    print(user)
    result = await create_user(user)
    if not result: raise HTTPException(400)
    return ("register successful")

@app.get("/api/get-task/{id}", response_model=Task)
async def get_one_task(id):
    task = await fetch_one_task(id)
    if not task: raise HTTPException(404)
    return task

@app.get("/api/get-task")
async def get_tasks():
    tasks = await fetch_all_tasks()
    if not tasks: raise HTTPException(404)
    return tasks

@app.post("/api/add-task", response_model=Task)
async def add_task(task: Task):
    result = await create_task(task)
    if not result: raise HTTPException(400)
    return result

@app.put("/api/update-task/{id}", response_model=Task)
async def update_task(task: Task):
    result = await change_task(task)
    if not result: raise HTTPException(400)
    return result

@app.delete("/api/delete-task/{id}")
async def delete_task(id):
    result = await remove_task(id)
    if not result: raise HTTPException(400)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
    
