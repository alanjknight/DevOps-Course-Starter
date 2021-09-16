import os
import requests
from dotenv import load_dotenv


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

def get_list_for_card(card_id):
    url = "https://api.trello.com/1/cards/" + card_id + "/list"
    response = run_get_query(url)
    return response.json()['name']

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


def delete_trello_task(id_long):
    url = "https://api.trello.com/1/cards/" + id_long 
     
    response = requests.request(
        "DELETE",
        url,
        headers=headers,
        params=query
    )
    print(response.text)
