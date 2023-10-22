from fastapi import FastAPI, HTTPException, UploadFile, Request, Form, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, Response
from typing import Annotated, List
import uvicorn
from database_todo import *
from database_login import *
from database_train import *
import json

origins = ["*"] 
# This will eventually be changed to only the origins you will use once it's deployed, to secure the app a bit more.

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# convert list into tuple
def convert_list_tuple(list):
    return tuple(list)

# convert json to list
def convert_json_list(file_name):
    result_list =[]
    with open(file_name, mode='r') as f:
        json_data = json.load(f)
        for i in json_data:
            result_list.append(json_data[i])
        f.close()
    return (result_list)

# Daily Train Table
headings = ("User", "Date", "푸쉬업", "배운동","벽스퀏", "팔운동","상체들기","뒤꿈치들기","의자발차기","무릎벌리기","Actions")
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

@app.get('/train')
async def get_train_data(request: Request):
    results = await fetch_all_trains()
    print(results)
   
    if not results: return{"msg":"no records found"}
    return templates.TemplateResponse("traintable.html", {"request": request, "headings": headings, "data": results}) 

@app.get('/train/{id}',response_model=Train)
async def get_train_data_byid(train: Train):
    train = await fetch_one_train(id)
    if not train: raise HTTPException(400)
    return train

@app.post('/train', response_model=FormData)
async def add_train_data(form_data: FormData = Body(...)):
    print(form_data)
    result = await create_train(form_data)
    print(result)
    if not result: raise HTTPException(400)
    return result

@app.delete("/train/{id}")
async def delete_train_byid(id):
    result = await delete_train(id)
    if not result: raise HTTPException(400)
    return result

@app.get("/uploadtrain")
def root(request: Request):
    print("request received")
    return templates.TemplateResponse("upload_train.html", {"request": request} )

@app.post('/register', response_model=Login)
async def user_register(id: Annotated[str, Form()], pw: Annotated[str, Form()]):
    user = {"id": id, "pw": pw}
    result = await create_user(user)
    if not result: raise HTTPException(400)
    return (user)

@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request} )
  
@app.post('/login', response_model=Login)
async def login_process(id: Annotated[str, Form()], pw: Annotated[str, Form()]):
    print(id, pw)
    result = await find_user(id)
    if not result: raise HTTPException(400)
    if not result['pw'] == pw: raise HTTPException(400)
    return (result)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
    
