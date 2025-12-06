from sqlalchemy import func
from typing import Optional

#______________Import Dependencies___________________

from .Rep import Rep
from Py_Models.Boards import Py_Boards
from Models.Models import Board, User

class Boards_Rep(Rep):

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self
    
    def __exit__(self,tb,val,ke):
        self.db.close()
    
    #______________Add new User___________________

    def Add_Board(self, board : Py_Boards) -> Optional[Board]:
        board = Board(** board.model_dump(exclude=['fields_list']))
        try:
            self.db.add(board)
            self.db.commit()
            self.db.refresh(board)
            return board
        except:
            return None
        
    #______________Authentication_________________

    def All_Boards(self) -> list[Py_Boards]:
        try:
            all_boards = self.db.query(Board.id , Board.title , Board.creation_date , User.username).join(User , User.id == Board.created_by).all()
            return [{ "id" : obj[0] , "title" : obj[1], "creation_date" : obj[2] , "created_by" : obj[3]} for obj in all_boards] # convert orm to pydantic class

        except Exception as e:
            return None
