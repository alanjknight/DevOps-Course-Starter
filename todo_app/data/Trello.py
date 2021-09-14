import requests
from dotenv import load_dotenv

from todo_app.data.Trello_API_helper import get_member_details
from todo_app.data.Trello_API_helper import get_board_details
from todo_app.data.Trello_API_helper import get_list_for_card
from todo_app.data.Trello_API_helper import get_lists_on_board
from todo_app.data.Trello_API_helper import get_cards_on_list
from todo_app.data.Trello_API_helper import get_cards_on_board
from todo_app.data.Trello_API_helper import write_new_task_status
from todo_app.data.Trello_API_helper import add_trello_task
from todo_app.data.Trello_API_helper import delete_trello_task
from todo_app.data.Trello_API_helper import run_get_query

from todo_app.data.Trello_Member import Trello_Member
from todo_app.data.Trello_Board import Trello_Board
from todo_app.data.Trello_List import Trello_List
from todo_app.data.Trello_Item import Trello_Item

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


def update_task_status(id_long, action):
    task = get_card(id_long)
    new_list_name = get_listname_by_action(action)
    new_list = get_list_by_list_name(task.board_id, new_list_name)
    write_new_task_status(task,new_list)
    
def add_task(title, target_date):
    member = get_member('alanjknight@hotmail.com')
    #assuming one board, and assume all new tickets go on todo list
    get_boards_for_member(member)
    board_id = member.board_list[0].id
    l = get_list_by_list_name(board_id, "To Do")
    add_trello_task(title, target_date, board_id, l.id)

def delete_task(id_long):
    delete_trello_task(id_long)
