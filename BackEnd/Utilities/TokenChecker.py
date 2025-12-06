import jwt

#___________________Cach Functions____________________

from Utilities.JWT_Config import JWT_Config

#____________Import FastAPI Resources_________________

from functools import lru_cache
from fastapi import Request , status
from fastapi.exceptions import HTTPException

#_________________Cach JWT Token_______________________

@lru_cache
def cach_jwt_config():
    return JWT_Config()

#___handle the Authority of all user's requests_______

def Check_Token(request : Request):
    try:

        jwt_conf = cach_jwt_config() # read jwt config from cach
        
        #____________________Check Tokens validity and Authorization__________________________

        if not request.headers.get('X-Token') or request.headers.get('X-Token') is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail = "Token is Invalid")
        else:
            token = request.headers.get('X-token') # user token that is embedded in X-token header
            try:
                jwt.decode(token , jwt_conf.key , jwt_conf.algorithm) # if token be invalid, this function will raise a HTTP Exception
            except: 
                raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail = "Token is Invalid") # token has been expired!
            
    except Exception as error:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail = "Token is Invalid")