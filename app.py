from flask import Flask, render_template, redirect, url_for, request
from os import urandom
from flask_sqlalchemy import SQLAlchemy
from requests import get
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_task.db'

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("layout.html")


@app.route('/request', methods=['GET'])
def req():
    count = 2
    req = get(f"https://jservice.io/api/random?count={count}").json()
    print(req)
    return render_template("layout.html")


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
