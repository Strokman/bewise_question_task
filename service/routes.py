from service import app
from flask import request
from .models import JServiceApiHandler


@app.route('/count', methods=['GET', 'POST'])
def count():
    questions_num = request.json.get('questions_num')
    resp = JServiceApiHandler(questions_num)
    print(resp.ready_data)
    resp.commit_to_db()
    # print(resp.json_data())
    return '', 200
