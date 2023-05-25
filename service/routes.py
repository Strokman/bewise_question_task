from service import app
from flask import request
from requests import get
from .models import JServiceApiQuestion, make_request, check_question_exists, get_last_question


@app.route('/count', methods=['GET', 'POST'])
def count():
    last_question = get_last_question()
    questions_num = request.json.get('questions_num')
    if questions_num < 101:
        req: list = get(f"https://jservice.io/api/random?count={questions_num}").json()
        for item in req:
            a = JServiceApiQuestion(item)
            if not check_question_exists(a.processed_data.get('id')):
                print(check_question_exists(a.processed_data.get('id')))
                a.commit_to_db()
            else:
                b = JServiceApiQuestion(make_request())
                b.commit_to_db()
        return last_question
    else:
        return "Too many questions requested, questions_num should be <= 100", 405
