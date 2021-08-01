import os
import requests
from dotenv import load_dotenv
from todo_app.data.Trello_Member import Trello_Member
from todo_app.data.Trello_Board import Trello_Board
from todo_app.data.Trello_List import Trello_List
from todo_app.data.Trello_Item import Trello_Item


load_dotenv()
TRELLO_KEY = os.getenv('TRELLO_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')

headers = {
   "Accept": "application/json"
}

query = {
   'key' :  TRELLO_KEY,
   'token' : TRELLO_TOKEN
}

def run_get_query(url):
    return requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )


def get_member_details(user_id):
    url = "https://api.trello.com/1/members/" + user_id
    return run_get_query (url)

def get_board_details(board_id):
    url = "https://api.trello.com/1/boards/" + board_id
    return run_get_query (url)

def get_board_lists(board_id):
    url = "ttps://api.trello.com/1/boards/" + board_id + "/lists"
    return run_get_query (url)

def get_cards_on_list(list_id):
    url = "https://api.trello.com/1/lists/" + list_id + "/cards"
    return run_get_query(url)

def get_lists_on_board(board_id):
    url = "https://api.trello.com/1/boards/" + board_id + "/lists"
    return run_get_query(url)

def get_cards_on_board(board_id):
    url = "https://api.trello.com/1/boards/" + board_id + "/cards"
    return run_get_query(url)

def get_list_for_card(card_id):
    url = "https://api.trello.com/1/cards/" + card_id + "/list"
    response = run_get_query(url)
    return response.json()['name']

def get_member(member_id):
    response = get_member_details(member_id)
    return Trello_Member(response.json()['username'], response.json()['fullName'], response.json()['idBoards'])

def get_card(task_id):
    url = "https://api.trello.com/1/cards/" + task_id
    response = run_get_query (url)
    card = response.json()
    return Trello_Item(card['id'], card['idShort'] , get_list_for_card(card['id']), card['name'], card['due'], card['idBoard'])


def add_board_to_member(member,board_id):
    response = get_board_details(board_id)
    member.add_board(Trello_Board(response.json()['id'], response.json()['name']))
    
    
def add_lists_to_board(board):
    response = get_lists_on_board(board.id)
    for list in response.json():
        l = Trello_List(list['id'], list['name'])
        board.add_list(l)

def add_cards_to_board(board):
    response = get_cards_on_board(board.id)
    for card in response.json():
        c = Trello_Item(card['id'], card['idShort'], get_list_for_card(card['id']), card['name'], card['due'], card['idBoard'])
        board.add_card(c)
    
def add_cards_to_list(list):
    response = get_cards_on_list(list.id)
    for card in response.json():
        c = Trello_Item(card['id'], card['idShort'] , list.name, card['name'], card['due'], card['idBoard'])
        list.add_card(c)

def get_boards_for_member(member):
    for board_id in member.board_id_list:
        add_board_to_member(member,board_id)


def hydrate_member(member):
    get_boards_for_member(member)    
    for board in member.board_list:    
        add_lists_to_board(board)
        add_cards_to_board(board)
        for list in board.lists_list:
            add_cards_to_list(list)

def get_listname_by_action(action):
    if action=="start_task":
        return "Doing"
    elif action=="finish_task":
        return "Done"
    elif action=="reset_task":
        return "To Do"
    return None

def get_list_by_list_name(board_id, name):
    response = get_lists_on_board(board_id)
    for l in response.json():
        if l['name'] == name:
            return Trello_List(l['id'], l['name'])
    return None

def write_new_task_status(task, list):
    url = "https://api.trello.com/1/cards/" + task.id_long 
    query = {
        'key' :  TRELLO_KEY,
        'token' : TRELLO_TOKEN,
        'idList' : list.id
    } 
    response = requests.request(
        "PUT",
        url,
        headers=headers,
        params=query
    )


def update_task_status(id_long, action):
    task = get_card(id_long)
    new_list_name = get_listname_by_action(action)
    new_list = get_list_by_list_name(task.board_id, new_list_name)
    write_new_task_status(task,new_list)
    

    
def delete_task_from_board(id_long):
    url = "https://api.trello.com/1/cards/" + id_long 
     
    response = requests.request(
        "DELETE",
        url,
        headers=headers,
        params=query
    )
    print(response.text)


def add_trello_task(title, target_date, board_id, list_id):
    url = "https://api.trello.com/1/cards" 
   
    query = {
      'key' :  TRELLO_KEY,
      'token' : TRELLO_TOKEN,
      'idList' : list_id,
      'name': title,
      'due': target_date,
    } 
    
    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )
    print(response.text)

def add_task(title, target_date):
    member = get_member('alanjknight@hotmail.com')
    #assuming one board, and assume all new tickets go on todo list
    
    get_boards_for_member(member)
    board_id = member.board_list[0].id
    l = get_list_by_list_name(board_id, "To Do")
    add_trello_task(title, target_date, board_id, l.id)

    


#########tests################################
#member = get_member('alanjknight@hotmail.com')
#for board_id in member.board_id_list:
#    add_board_to_member(member,board_id)
#    
#for board in member.board_list:    
#    add_lists_to_board(board)
#    add_cards_to_board(board)
#    for list in board.lists_list:
#        add_cards_to_list(list)#

#print(member.to_string())
