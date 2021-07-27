class Trello_Board:

    def __init__(self, id, name):
        self.id=id
        self.name=name
        self.lists_list = []
        self.item_list = []

    def add_list(self, list):
        self.lists_list.append(list)

    def add_card(self, list):
        self.item_list.append(list)

    def to_string(self):
        s = self.id + " " + self.name + " " 
        for list in self.lists_list:
            s = s + list.to_string() 
        for item in self.item_list:
            s = s + item.to_string()   
        return s 