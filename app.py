from flask import Flask, render_template, redirect, url_for, request
from os import urandom
from flask_sqlalchemy import SQLAlchemy
from models import Jserviceapihandler

app = Flask(__name__)

app.config['SECRET_KEY'] = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_task.db'

db = SQLAlchemy(app)


@app.route('/<question_num>', methods=['POST'])
def index(question_num):
    question_num = question_num
    print(question_num)
    return question_num


@app.route('/count', methods=['GET', 'POST'])
def count():
    # title = 'How much questions?'
    resp = Jserviceapihandler(request.json.get('questions_num'))
    print(resp.json_data())
    return resp.json_data()
    #
    # print(resp.json_data())
    #
    # return resp.json_data(), 200
    # return render_template("count.html", title=title, form=form)


# @app.route('/request')
# def req():
#     resp = Jserviceapihandler(count)
#     print(resp.json_data())
#     return render_template("layout.html")


if __name__ == '__main__':
    app.run(debug=True)
