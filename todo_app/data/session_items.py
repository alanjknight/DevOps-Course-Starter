from flask import session
from datetime import datetime

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'Task1', 'target_date': datetime.strptime('1/7/14','%d/%m/%y')},
    { 'id': 2, 'status': 'Not Started', 'title': 'Task2', 'target_date': datetime.strptime('1/7/15','%d/%m/%y')},
    { 'id': 3, 'status': 'Not Started', 'title': 'Task3', 'target_date': datetime.strptime('1/7/16','%d/%m/%y')},
    { 'id': 4, 'status': 'Not Started', 'title': 'Task4', 'target_date': datetime.strptime('1/7/17','%d/%m/%y')},
    { 'id': 5, 'status': 'Not Started', 'title': 'Task5', 'target_date': datetime.strptime('1/7/18','%d/%m/%y')},
    { 'id': 6, 'status': 'Not Started', 'title': 'Task6', 'target_date': datetime.strptime('1/7/19','%d/%m/%y')},
    { 'id': 7, 'status': 'Not Started', 'title': 'Task7', 'target_date': datetime.strptime('1/7/20','%d/%m/%y')},
    { 'id': 8, 'status': 'Not Started', 'title': 'Task8', 'target_date': datetime.strptime('1/7/21','%d/%m/%y')}
]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get('items', _DEFAULT_ITEMS.copy())


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title, target_date):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' , 'target_date': target_date}

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def delete_item(id):
    items = get_items()
    item = get_item(id)
    items.remove(item)
    session['items'] = items

