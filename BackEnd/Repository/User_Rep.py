import hashlib
import sqlalchemy
from typing import Optional

#______________Import Dependencies___________________

from .Rep import Rep
from Py_Models.Users import Py_Users
from Models.Models import User

class User_Rep(Rep):

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self
    
    def __exit__(self,tb,val,ke):
        self.db.close()
    
    #______________Add new User___________________

    def Register(self, usr : Py_Users) -> Optional[User]:
        user = User(** usr.model_dump())
        user.password = str(hashlib.md5(str(user.password).encode("UTF-8")).digest()) # hash password
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except:
            return None
        
    #______________Authentication_________________

    def Authenticate(self , username : str , password : str) -> Optional[User]:
        try:
            pass1 = (str(hashlib.md5(str(password).encode("UTF-8")).digest())) # hash password at first    
            obj = (self.db.query(User).filter(sqlalchemy.and_(User.username == username , User.password == pass1)).first()) # return actived users here

            if(obj): # obj1 isn't null
                return obj
            else:
                None 
        except Exception as e:
            print(f'An unexpected error during login process: {e}')
            return None
        
    #_______________Update User___________________

    def change_password(self, user : Py_Users, new_password : str) -> int:
        try:
            obj = self.Authenticate(user.email , user.password)                
            obj.password = str(hashlib.md5(str(new_password).encode("UTF-8")).digest())
            self.db.commit()
            return 1
        except:
            return -1
        
