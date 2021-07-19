from todo_app.data.session_items import add_item, get_items, get_item, save_item, delete_item
from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime

from operator import itemgetter

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

def update_task_status(task, action):
    if action=="start_task":
        task["status"]="Started"
    if action=="finish_task":
        task["status"]="Finished"    
    if action=="reset_task":
        task["status"]="Not Started"    
    save_item(task)

def is_sort_reverse(sort_col, last_sort_col):
    sort_reverse = request.args.get('sort_reverse', session.get('sort_reverse'))
    sort_reverse = (sort_reverse=='True')   
    
    if last_sort_col == sort_col:
        sort_reverse = not sort_reverse
    else:
        sort_reverse = False 

    return sort_reverse

def get_last_sort_col():
    return request.args.get('last_sort_col', session.get('last_sort_col', 'id'))
    
def get_sort_col():
    return request.args.get('sort_col', session.get('sort_col', 'id'))

@app.route('/', methods = ['GET'])
def index():
    
    sort_col=get_sort_col()
    last_sort_col=get_last_sort_col()
    sort_reverse = is_sort_reverse(sort_col, last_sort_col)
    print (sort_col, last_sort_col, sort_reverse)
    last_sort_col=sort_col    
    
    items = get_items()
    items = sorted(items,key=itemgetter(sort_col), reverse=sort_reverse)

    entered_title = session.get('entered_title')
    entered_target_date = session.get('entered_target_date')
    target_date_feedback = session.get('target_date_feedback')
    title_feedback = session.get('title_feedback')
    session['entered_title']=""
    session['entered_target_date'] = ""
    session['target_date_feedback'] = ""
    session['title_feedback'] = ""


    return render_template('index.html', items=items, 
        last_sort_col=last_sort_col, 
        sort_reverse=sort_reverse,
        entered_title = entered_title,
        entered_target_date = entered_target_date,
        target_date_feedback = target_date_feedback,
        title_feedback = title_feedback)

@app.route('/', methods = ['POST'])
def submit():
    title_feedback = ""
    target_date_feedback = ""

    target_date = 0
    input_error = False

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

    session['last_sort_col'] = request.form['last_sort_col'] 
    session['sort_reverse'] = request.form['sort_reverse']
    session['sort_col']=request.form['last_sort_col']
 
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
    return redirect(url_for('index'))
    
@app.route('/delete/<int:id>')
def delete_task(id):
    delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
