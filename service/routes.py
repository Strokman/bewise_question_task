from service import app, db
from flask import request
from .models import Jserviceapihandler, Question
from datetime import datetime
#
# @app.route('/<question_num>', methods=['POST'])
# def index(question_num):
#     question_num = question_num
#     print(question_num)
#     return question_num


@app.route('/count', methods=['GET', 'POST'])
def count():
    # title = 'How much questions?'
    questions_num = request.json.get('questions_num')
    resp = Jserviceapihandler(questions_num)
    # print(resp.json_data())
    for i in resp.json_data():
        temp = dict()
        for k, v in i.items():
            if k in ['id', 'question', 'answer', 'created_at', 'category_id']:
                temp[k] = v
        temp['created_at'] = datetime.strptime(temp['created_at'].replace('Z', '').replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f')
        question = Question(temp['id'], temp['question'], temp['answer'], temp['created_at'], temp['category_id'])
        db.session.add(question)
        db.session.commit()
    print(temp, type(temp['created_at']))
    return 'Success!', 200
