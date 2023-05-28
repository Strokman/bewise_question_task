from questions import app
from flask import request
from requests import get
from .helpers import make_request, check_question_exists, get_last_question
from .models import JServiceApiQuestion


@app.route('/count', methods=['POST'])
def count():
    """
    View принимает запрос по методу POST с аргументом
    question_num: int, после чего запрашивает у API jservice
    нужное количество вопросов. Принимает число не более 100, так как за один раз
    макс. количество запрашиваемых вопросов у jservice не может быть более 100
    :return:
    """
    last_question: str = get_last_question()
    questions_num: int = request.json.get('questions_num')
    if 0 < questions_num < 101:
        resp: list = get(f"https://jservice.io/api/random?count={questions_num}").json()
        for item in resp:
            question = JServiceApiQuestion(item)
            if not check_question_exists(question.processed_data.get('id')):
                question.commit_to_db()
            else:
                another_question = JServiceApiQuestion(make_request())
                another_question.commit_to_db()
        return last_question
    else:
        return "Please provide correct number of questions: 0 < questions_num < 100", 405
