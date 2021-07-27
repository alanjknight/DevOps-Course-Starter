#'id': 1, 'status': 'Not Started', 'title': 'Task1', 'target_date': datetime.strptime('1/7/14','%d/%m/%y')},

class Trello_Item:
    def __init__(self, id_long, id, status, title, target_date):
        self.id=int(id)
        self.id_long=id_long
        self.status=status
        self.title=title
        self.target_date=target_date
        

    def to_string(self):
        s = str(self.id) + " " + str(self.id_long) + " " + self.status + " " + self.title + " " + self.target_date + " "
        return s 
