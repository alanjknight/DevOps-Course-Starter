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
        c = Trello_Item(card['id'], card['idShort'] , get_list_for_card(card['id']), card['name'], card['due'])
        board.add_card(c)

def add_cards_to_list(list):
    response = get_cards_on_list(list.id)
    for card in response.json():
        c = Trello_Item(card['id'], card['idShort'] , list.name, card['name'], card['due'])
        list.add_card(c)


def hydrate_member(member):
    for board_id in member.board_id_list:
        add_board_to_member(member,board_id)
        
    for board in member.board_list:    
        add_lists_to_board(board)
        add_cards_to_board(board)
        for list in board.lists_list:
            add_cards_to_list(list)



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
 




