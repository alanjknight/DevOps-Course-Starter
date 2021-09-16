class Trello_List:

    def __init__(self, id, name):
        self.id=id
        self.name=name
        self.item_list=[]
        
    def add_card(self, list):
        self.item_list.append(list)

    def to_string(self):
        s = self.id + " " + self.name  + " " 
        for item in self.item_list:
            s = s + item.to_string() 

        return s 
