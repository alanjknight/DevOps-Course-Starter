from todo_app.data.Trello_Member import Trello_Member
from todo_app.data.Trello_Item import Trello_Item


class ViewModel:
    def __init__(self, member,sort_col,last_sort_col,sort_dir,entered_title,entered_target_date, target_date_feedback,title_feedback):
        self._member = member
        self._sort_col=sort_col
        self._last_sort_col=last_sort_col
        self._sort_dir=sort_dir
        self._entered_title=entered_title
        self._entered_target_date=entered_target_date
        self._target_date_feedback=target_date_feedback
        self._title_feedback=title_feedback
    
    @property
    def member(self):
        return self._member

    @property
    def sort_col(self):
        return self._sort_col

    @property
    def last_sort_col(self):
        return self._last_sort_col

    @property
    def sort_dir(self):
        return self._sort_dir

    @property
    def entered_title(self):
        return self._entered_title

    @property
    def entered_target_date(self):
        return self._entered_target_date

    @property
    def target_date_feedback(self):
        return self._target_date_feedback

    @property
    def title_feedback(self):
        return self._title_feedback

    def get_items(self, status):
        l=[]
        for item in self._member.board_list[0].item_list:
            if item.status == status:
                l.append(item)
        return l        
