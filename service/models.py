from requests import get
from service import db


class Jserviceapihandler:

    def __init__(self, count):
        self.count = count
        self.__data = get(f"https://jservice.io/api/random?count={count}")

    def json_data(self):
        return self.__data.json()


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    question_id = db.Column(db.Integer(), nullable=False, unique=True)
    question_text = db.Column(db.String(100), nullable=False)
    question_answer = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer(), nullable=False)

    def __init__(self, question_id, question_text, question_answer, created_at, category_id):
        self.question_id = question_id
        self.question_text = question_text
        self.question_answer = question_answer
        self.created_at = created_at
        self.category_id = category_id






