import jwt
import asyncio
import uvicorn
from typing import Annotated
from datetime import datetime , timedelta , timezone

#_______________FastAPI Libraries__________________

from fastapi import FastAPI , Body , Depends, WebSocket
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect

from Py_Models.Users import Py_Users
from Data_Layer.Redis_DB import RealTimeList
from Utilities.JWT_Config import JWT_Config

#_______________Import Repositories_________________

from Repository.User_Rep import User_Rep
from Repository.Boards_Rep import Boards_Rep

#_______________Import Token Checker________________

from Utilities.TokenChecker import Check_Token

#__________________Import Routes____________________

from Back_Routes.State_Of_Art_Boards_Route import boards_route
from Back_Routes.Quick_Win_Boards_Route import qw_boards_route

#________________Const Objects_______________________

from Back_Routes.State_Of_Art_Boards_Route import ws_manager
from Back_Routes.State_Of_Art_Boards_Route import streamer_task

RedisDB = RealTimeList() # instanciate a new object from Redis Database as a Real-Time Database

app = FastAPI() # main object
app.include_router(router = boards_route , dependencies=[Depends(Check_Token)])
app.include_router(router = qw_boards_route)

#______________Define Cors MiddleWare_______________

app.add_middleware(
                   CORSMiddleware , 
                   allow_origins = ["http://localhost:3000"] , 
                   allow_credentials = True , 
                   allow_methods = ['*'] , 
                   allow_headers = ["X-Token",'Content-Type'],
                   expose_headers=["Access-Control-Expose-Headers"]  # Corrected placement
                )

#________Start Redis Listener on startup_____________

streamer_task = [] # main streamer

async def start_up():
    with Boards_Rep() as boards_rep:
        boards = boards_rep.All_Boards()
        global streamer_task
        for board in boards:
            streamer_task.append(asyncio.create_task(RedisDB.Streamer(board['id'], ws_manager)))

app.add_event_handler("startup" , start_up)

#_____________Handle Web-Socket______________________

@app.websocket('/ws/boards/{board_id}')
async def connect_consumers(board_id : int, websocket : WebSocket):
    await ws_manager.connect(board_id=board_id, websocket=websocket) # connect users
    try:
        while True: # keep all users connected
            await websocket.receive_text()  # keep connection alive with user        
            tasks = await RedisDB.all_tasks(board_id)
            await websocket.send_json(tasks)

    except WebSocketDisconnect:
        await ws_manager.disconnect(board_id, websocket)

#_____________Authentication Process___________________

def create_token(id : int , username : str):
    jwt_conf = JWT_Config() # load jwt config from env file
    exp_date = datetime.now(timezone.utc) + timedelta(days = jwt_conf.token_expire_time)  # expiration date

    payload = {
                "sub": id,# subject (user id)
                "username": username,
                "iat": datetime.now(timezone.utc),
                "exp": exp_date
            }

    token = jwt.encode(payload, jwt_conf.key , jwt_conf.algorithm) # return jwt token
    return {"token" : token , "username" : username, "id" : id ,"exp" : jwt_conf.token_expire_time}


@app.post('/Authenticate')
def login(username : Annotated[str , Body()] , password : Annotated[str , Body()]):
    try:
        
        with User_Rep() as user_rep: # user repository context manager
            result = user_rep.Authenticate(username , password)

        if result == None: # user doesn't exist
            raise HTTPException(status_code=401, detail="Invalid username and/or password")
        else:

            #____________create a new JWT Token________________

            return create_token(result.id , username)
        
    except:
        return None


#_____________User Registeration Process__________________

@app.post('/SignUp')
def register(user: Annotated[Py_Users , Body()]):
    try:
        with User_Rep() as user_rep: # Register New User
            result = user_rep.Register(user)
        
        if (result):
            return create_token(result.id , user.username) # create a token and return if registeration process have been successfull
        else:
            raise HTTPException(status_code = 409, detail = "The user with Username/email does already exist!")

    except:
        raise HTTPException(status_code = 500, detail = "An error has occurred, please try again later.")


#___________Run Uvicorn Sever on port 8000________________

#if __name__ == '__main__':
#    uvicorn.run(app , port = 8000 , host = 'localhost')