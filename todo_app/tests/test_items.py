from todo_app.ViewModel import ViewModel
from todo_app.data.Trello_Member import Trello_Member
from todo_app.data.Trello import get_member, hydrate_member, update_task_status, delete_task, add_task

#test we are only getting 'to do' items
def test_only_to_do_items():
    #Arrange
    member = get_member('alanjknight@hotmail.com')
    
    #Act
    hydrate_member(member)
    vm = ViewModel(member,None,None,None,None,None,None,None)
    items = vm.get_ToDo_items()

    #Assert we only have items in TODO Status
    for item in items:
        assert item.status == "To Do"
        
def test_only_doing_items():
    #Arrange
    member = get_member('alanjknight@hotmail.com')
    
    #Act
    hydrate_member(member)
    vm = ViewModel(member,None,None,None,None,None,None,None)
    items = vm.get_doing_items()

    #Assert 
    for item in items:
        assert item.status == "Doing"


def test_only_done_items():
    #Arrange
    member = get_member('alanjknight@hotmail.com')
    
    #Act
    hydrate_member(member)
    vm = ViewModel(member,None,None,None,None,None,None,None)
    items = vm.get_done_items()

    #Assert 
    for item in items:
        assert item.status == "Done"