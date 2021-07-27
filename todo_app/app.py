from todo_app.flask_config import Config
from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
from operator import itemgetter
from todo_app.data.Trello_Member import Trello_Member
from todo_app.data.Trello_Loader import get_member, hydrate_member

app = Flask(__name__)
app.config.from_object(Config)

#def update_task_status(task, action):
#    if action=="start_task":
#        task["status"]="Started"
#    if action=="finish_task":
#        task["status"]="Finished"    
#    if action=="reset_task":
#        task["status"]="Not Started"    
#    save_item(task)

def get_last_sort_col():
    #could not get these lines to return the default of when last_sort_col was None in agrs and session.
#    return request.args.get('last_sort_col', session.get('last_sort_col', 'id'))
    lsc = request.args.get('last_sort_col')
    if not lsc:
        lsc = session.get('last_sort_col')
    if not lsc:
        lsc = 'id'
    return lsc
    
def get_sort_col():
    #as in get last sort col, cant get the defaults to work.
    #print("Sort Col", request.args.get('sort_col', session.get('sort_col', 'id')))
    #return request.args.get('sort_col', session.get('sort_col', 'id'))
    sc = request.args.get('sort_col')
    if not sc:
        sc = session.get('sort_col')
    if not sc:
        sc = "id"
    return sc


def get_sort_dir():
    sd = request.args.get('sort_dir')
    if not sd:
        sd = session.get('sort_dir')
    if not sd:
        sd = 'asc'
    return sd    

def preserve_sort():
    pso = session.get('preserve_sort')
    session['preserve_sort']=None
    return pso==True

def get_sort_parameters():
    
    if(not request.args.get('sort_col') and not session.get('sort_col')):
        sort_col='id'
        last_sort_col=None
        sort_reverse=False
        sort_dir='asc'
        return sort_col, last_sort_col, sort_reverse, sort_dir    
    else:
        sort_col = get_sort_col()
        last_sort_col = get_last_sort_col()
        sort_dir = get_sort_dir()
        if(not preserve_sort()):
            if (sort_col == last_sort_col):
                if (sort_dir == 'asc'):
                    sort_dir='des'
                else:
                    sort_dir='asc'    
        if sort_dir == 'asc':
            sort_reverse = False
        else:
            sort_reverse = True

        last_sort_col=sort_col    
        return sort_col, last_sort_col, sort_reverse, sort_dir
    

@app.route('/', methods = ['GET'])
def index():
    
    member = get_member('alanjknight@hotmail.com')
    hydrate_member(member)
 
    sort_col, last_sort_col, sort_reverse, sort_dir = get_sort_parameters()
    
    if(sort_col=='id'):
        member.board_list[0].item_list = sorted(member.board_list[0].item_list,key=lambda item: item.id, reverse=sort_reverse)
    elif(sort_col=='title'):
        member.board_list[0].item_list = sorted(member.board_list[0].item_list,key=lambda item: item.title, reverse=sort_reverse)
    elif(sort_col=='status'):
        member.board_list[0].item_list = sorted(member.board_list[0].item_list,key=lambda item: item.status, reverse=sort_reverse)
    elif(sort_col=='target_date'):
        member.board_list[0].item_list = sorted(member.board_list[0].item_list,key=lambda item: item.target_date, reverse=sort_reverse)        

    
#    entered_title = session.get('entered_title')
#    entered_target_date = session.get('entered_target_date')
#    target_date_feedback = session.get('target_date_feedback')
#    title_feedback = session.get('title_feedback')
#    session['entered_title']=""
#    session['entered_target_date'] = ""
#    session['target_date_feedback'] = ""
#    session['title_feedback'] = ""

    
    return render_template('index.html', member=member, 
        sort_col=sort_col,
        last_sort_col=last_sort_col, 
        sort_dir=sort_dir)

#       entered_title = entered_title,
#       entered_target_date = entered_target_date,
#       target_date_feedback = target_date_feedback,
#       title_feedback = title_feedback)

"""
@app.route('/', methods = ['POST'])
def submit():
    title_feedback = ""
    target_date_feedback = ""

    target_date = 0
    input_error = False

    session['last_sort_col'] = request.form['last_sort_col'] 
    session['sort_dir']=request.args.get('sort_dir')
    session['sort_col']=request.form['last_sort_col']

    if not request.form['title']:
        input_error = True
        title_feedback = "Cannot add a ToDo item without a title"
    
    if not request.form['target_date']:
        input_error = True
        target_date_feedback = "Cannot add a ToDo item without a target date"
    else:
        try:
            target_date = datetime.strptime(request.form['target_date'],'%d/%m/%y')
        except:
            input_error = True
            target_date_feedback = "This date cannot be converted to a date in the format dd/mm/yy"

 
    if input_error:
        session['entered_title'] = request.form['title']
        session['entered_target_date'] = request.form['target_date']
        session['target_date_feedback'] = target_date_feedback
        session['title_feedback']=title_feedback
        return redirect(url_for('index'))

    add_item(request.form['title'], target_date)
    return redirect(url_for('index'))

@app.route('/update/<string:action>/<int:id>')
def update_task(action, id):
    task = get_item(id)
    update_task_status(task, action)
    session['last_sort_col']=get_last_sort_col()
    session['sort_col']=get_sort_col()
    session['sort_dir']=request.args.get('sort_dir')
    session['preserve_sort']=True
    return redirect(url_for('index'))
"""    

@app.route('/delete/<int:id>')
def delete_task(id):
    delete_item(id)
    session['last_sort_col']=get_last_sort_col()
    session['sort_col']=get_sort_col()
    session['sort_dir']=request.args.get('sort_dir')
    session['preserve_sort']=True
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
