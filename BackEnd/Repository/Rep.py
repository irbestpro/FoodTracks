from Data_Layer.DB_Context import Session

class Rep():
    def __init__(self) :
        self.db = Session()