from todo_app.data.session_items import add_item, get_items
from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/', methods = ['POST'])
def submit():
    add_item(request.form['title'])
    return render_template('index.html', items=get_items())


if __name__ == '__main__':
    app.run()
