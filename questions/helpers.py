from questions import db
from .models import Question
from requests import get


def get_last_question() -> str:
    """
    Функция делает запрос к базе и возвращает последний
    добавленный в нее вопрос (сортирует выдачу по id в порядке убывания
    и берет первую запись)
    :return: str
    """
    try:
        last_q: str = db.session.query(Question).order_by(Question.id.desc()).first().as_json()
        return last_q
    except AttributeError:
        return " "


def check_question_exists(question_id: int) -> Question | None:
    """
    Функция получает на вход id вопроса и проверяет,
    есть ли такой вопрос в базе, возвращает его при
    положительном результате или None при отрицательном
    :param question_id:
    :return: Question | None
    """
    return db.session.execute(db.select(Question).filter_by(question_id=question_id)).scalar()


def make_request() -> dict:
    """
    Функция делает единичный запрос к API jservice
    и возвращает словарь с результатом
    :return: str
    """
    resp = get("https://jservice.io/api/random?count=1").json()[0]
    return make_request() if check_question_exists(resp.get('id')) else resp
