from service import app
from flask import request
from requests import get
from .models import JServiceApiQuestion, make_request, check_question_exists
from sqlalchemy import select
from requests.exceptions import JSONDecodeError


@app.route('/count', methods=['GET', 'POST'])
def count():
    questions_num = request.json.get('questions_num')
    req = get(f"https://jservice.io/api/random?count={questions_num}").json()
    for item in req:
        a = JServiceApiQuestion(item)
        if not check_question_exists(a.processed_data.get('id')):
            a.commit_to_db()
        else:
            print('make req activated')
            b = JServiceApiQuestion(make_request())
            b.commit_to_db()


    # questions = [item[0] for item in db.session.execute(select(Question.question_id)).all()]
    # print(questions)
    # questions_num = request.json.get('questions_num')
    # while questions_num > 0:
    #     # try:
    #     a = JServiceApiQuestion()
    #     if a.processed_data.get('id') in questions:
    #         questions_num += 1
    #     else:
    #         a.commit_to_db()
    #         questions_num -= 1
        # except JSONDecodeError:
        #
        #     print(a.data, a.processed_data)
        #     print('WHAT THE FUCK')
        #     continue
    return '', 200
