from todo_app.data.session_items import add_item, get_items, get_item, save_item, delete_item
from flask import Flask, render_template, request, redirect, url_for
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

    
@app.route('/', methods = ['GET'])
def index():
    
    sort_col="id"
    last_sort_col='id'
    sort_reverse='True'

    # which column are we to sort on (id passed in by default if nothing specified)
    if request.args.get("sort_col"):
        sort_col=request.args.get("sort_col")

    # is sorting to be reversed?  And convert the string value to a bool.
    if request.args.get("sort_reverse"):
        sort_reverse = request.args.get("sort_reverse")

    if sort_reverse == "True":
        sort_reverse = True
    else:
        sort_reverse = False    
    print("xx"+str(sort_reverse))

    #which column had we previosly sorted on (id passed in as default)
    #this is used to make sure that if we sorted on the same column as before, we reverse the sort order, if its different, we revert to ascending.
    if request.args.get("last_sort_col"):
        print('last_sort_col Request:'+request.args.get("last_sort_col"))
        last_sort_col=request.args.get("last_sort_col")

    if last_sort_col == sort_col:
        sort_reverse = not sort_reverse
    else:
        sort_reverse = False    

    last_sort_col=sort_col    
    
    items = get_items()
    items = sorted(items,key=itemgetter(sort_col), reverse=sort_reverse)

    return render_template('index.html', items=items, last_sort_col=last_sort_col, sort_reverse=sort_reverse)

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
    
    if input_error:
        return render_template('index.html',items=get_items(),
            entered_title=request.form['title'], entered_target_date=request.form['target_date'],
            target_date_feedback=target_date_feedback,title_feedback=title_feedback)
    
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
