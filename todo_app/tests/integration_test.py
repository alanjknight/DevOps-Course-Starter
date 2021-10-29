import pytest
from unittest.mock import patch, Mock

from dotenv import find_dotenv, load_dotenv 
from todo_app import app

@pytest.fixture

def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

sample_member_response = {"username":"Joe.Bloggs@xyz.com","fullName":"Joe Bloggs", "idBoards":["1"]}
sample_board_response= {"id":"1","name":"Joes Board"}
sample_lists_on_board_response = [{"id":"1", "name":"JoesList 1"}]
sample_cards_on_board_response = [{"id":"Card1", "idShort":"1", "name":"JoesList 1", "due":"1/1/2021", "idBoard":"1", "dateLastActivity":"31/12/2020"}]
sample_get_list_for_card_response = {"name":"JoesList 1"}
sample_get_cards_on_list_response = [{"id":"Card1", "idShort":"1", "name":"Card1", "due":"1/1/2021", "idBoard":"1", "dateLastActivity":"31/12/2020"}]

@patch('requests.request')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    assert(response.status=='200 OK')
    #ensure we get HTML
    assert(response.data.decode().startswith('<!doctype html>'))
    #ensure the user Joe.Bloggs in mentioned in the page
    assert(response.data.decode().find('Joe Bloggs') >=0 )


def mock_get_lists(method, url, headers, params):
    if url == f"https://api.trello.com/1/members/alanjknight@hotmail.com":
        response = Mock()
        response.json.return_value = sample_member_response
        return response

    if url == f"https://api.trello.com/1/boards/1":
        response = Mock()
        response.json.return_value = sample_board_response
        return response

    if url == "https://api.trello.com/1/boards/1/lists":
        response = Mock()
        response.json.return_value = sample_lists_on_board_response
        return response

    if url == "https://api.trello.com/1/boards/1/cards":
        response = Mock()
        response.json.return_value = sample_cards_on_board_response
        return response

    if url == "https://api.trello.com/1/cards/Card1/list":
        response = Mock()
        response.json.return_value = sample_get_list_for_card_response
        return response


    if url == "https://api.trello.com/1/lists/1/cards":
        response = Mock()
        response.json.return_value = sample_get_cards_on_list_response
        return response
    
    

    return None

