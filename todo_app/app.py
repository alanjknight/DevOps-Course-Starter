from todo_app.data.session_items import add_item, get_items, get_item, save_item
from flask import Flask
from flask import render_template
from flask import request

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



@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/', methods = ['POST'])
def submit():
    add_item(request.form['title'])
    return render_template('index.html', items=get_items())


@app.route('/update/<string:action>/<int:id>')
def update_task(action, id):
    task = get_item(id)
    _update_task(task, action)
    return render_template('index.html', items=get_items())

if __name__ == '__main__':
    app.run()
