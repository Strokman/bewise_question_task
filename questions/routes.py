from questions import app
from flask import request, abort, jsonify
from requests import get
from .helpers import make_request, check_question_exists, get_last_question
from .models import JServiceApiQuestion


@app.route('/api/count', methods=['POST'])
def count():
    """
    View принимает запрос по методу POST с аргументом
    question_num: int, после чего запрашивает у API jservice
    нужное количество вопросов. Принимает число не более 100, так как за один раз
    макс. количество запрашиваемых вопросов у jservice не может быть более 100.
    Затем программа перебирает словарь с вопросами, проверяет их на наличие в базе и
    при отрицательном результате - сохраняет в базе. Если вопрос есть в базе -
    совершает еще один дополнительный запрос к API jservice (рекурсивная функция make_request(),
    которая также проверяет вопрос на наличие в БД).
    :return:
    """
    last_question: dict = get_last_question()
    questions_num: int = request.json.get('questions_num')
    try:
        if 0 < questions_num < 101:
            resp: list = get(f'https://jservice.io/api/random?count={questions_num}').json()
            for item in resp:
                question = JServiceApiQuestion(item)
                if not check_question_exists(question.processed_data.get('id')):
                    question.commit_to_db()
                else:
                    another_question = JServiceApiQuestion(make_request())
                    another_question.commit_to_db()
            return jsonify(last_question)
        else:
            abort(405, description='Please provide correct number of questions: 0 < questions_num < 101')
    except TypeError:
        abort(400, description='Please provide correct request body - {"questions_num": <int>}')


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e), description='Please use correct route - http://host:port/api/count'), 404


@app.errorhandler(405)
def incorrect_num(e):
    return jsonify(error=str(e)), 405


@app.errorhandler(415)
def incorrect_header(e):
    return jsonify(error=str(e), description='Provide correct header - Content-Type: application/json'), 415
