from todo_app.data.session_items import add_item, get_items, get_item, save_item, delete_item
from flask import Flask, render_template, request, redirect, url_for


from operator import itemgetter

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

def _update_task(task, action):
    if action=="start_task":
        task["status"]="Started"
    if action=="finish_task":
        task["status"]="Finished"    
    if action=="reset_task":
        task["status"]="Not Started"    
    save_item(task)

    
@app.route('/', methods = ['GET'])
def index(last_sorted_col="id", sorted_reversed=0):

    return render_template('index.html', items=get_items(), last_sorted_col=last_sorted_col, sorted_reversed=sorted_reversed)

@app.route('/', methods = ['POST'])
def submit():
    title_feedback = ""
    if not request.form['title']:
        title_feedback = "Cannot add a ToDo item without a title"
    else:
        add_item(request.form['title'])
    return render_template('index.html', items=get_items(), title_feedback=title_feedback)

@app.route('/update/<string:action>/<int:id>')
def update_task(action, id):
    task = get_item(id)
    _update_task(task, action)
    
    return render_template('index.html', items=get_items())

@app.route('/delete/<int:id>')
def delete_task(id):
    delete_item(id)
    return redirect(url_for('index'))

@app.route('/sort/<string:column>')
def sort_tasks(column):

    items = get_items()
    sorted_reversed = request.args.get("sorted_reversed")
    
    if sorted_reversed == "True":
        sorted_reversed = True
    else:
        sorted_reversed = False    

    last_sorted_col=request.args.get("last_sorted_col")

    if last_sorted_col == column:
        sorted_reversed = not sorted_reversed
    else:
        sorted_reversed = False    
        
    items = sorted(items,key=itemgetter(column), reverse=sorted_reversed)
    
    return render_template('index.html', items=items, last_sorted_col=column, sorted_reversed=sorted_reversed)

if __name__ == '__main__':
    app.run()
