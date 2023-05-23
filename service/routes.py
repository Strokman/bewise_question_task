from service import app, db
from flask import request
from .models import JServiceApiQuestion, Question
from sqlalchemy import select
from requests.exceptions import JSONDecodeError


@app.route('/count', methods=['GET', 'POST'])
def count():
    questions_num = request.json.get('questions_num')
    a = JServiceApiQuestion(questions_num)
    print(a.data)
    print(a.processed_data)
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
