from todo_app.data.Trello_Board import Trello_Board
class Trello_Member:

    def __init__(self, user_name, full_name, board_id_list):
        self.user_name=user_name
        self.full_name=full_name
        self.board_id_list = board_id_list
        self.board_list=[]
        
    def add_board(self, board):
        self.board_list.append(board)

    def to_string(self):
        s = self.user_name + " " + self.full_name + " " + "boards:"
        for board in self.board_list:
            s = s + board.to_string() 
        return s 


