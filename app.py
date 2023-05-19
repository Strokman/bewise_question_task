from flask import Flask, render_template, redirect, url_for, request
from os import urandom
from flask_sqlalchemy import SQLAlchemy
from models import Jserviceapihandler
from forms import CountForm
from requests import get

app = Flask(__name__)

app.config['SECRET_KEY'] = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_task.db'

db = SQLAlchemy(app)


@app.route('/')
def index():
    title = "HELLO"
    text = 'HELLO WORLD'
    return render_template("layout.html", title=title, text=text)


@app.route('/count', methods=['GET', 'POST'])
def count():
    title = 'How much questions?'
    form = CountForm()
    if form.validate_on_submit():
        count_user = form.count.data
        print(type(count_user))
        resp = Jserviceapihandler(count_user)
        print(resp.json_data())
    return render_template("count.html", title=title, form=form)


# @app.route('/request')
# def req():
#     resp = Jserviceapihandler(count)
#     print(resp.json_data())
#     return render_template("layout.html")


if __name__ == '__main__':
    app.run(debug=True)
