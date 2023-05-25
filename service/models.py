from requests import get
from service import db
from datetime import datetime
from json import dumps
from sqlalchemy.exc import IntegrityError, PendingRollbackError

class JServiceApiQuestion:

    REQUIRED_COLUMNS = ('id', 'question', 'answer', 'created_at', 'category_id')
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(self, req):
        self.data = req
        self.processed_data = self.extract_needed_data()

    def extract_needed_data(self):
        d = {}
        for key, value in self.data.items():
            if key in self.REQUIRED_COLUMNS:
                d.setdefault(key, value)
        d['created_at'] = datetime.strptime(d['created_at'].replace('Z', '').replace('T', ' '), self.TIME_FORMAT)
        return d

    def commit_to_db(self):
        question = Question(self.processed_data.get('id'),
                            self.processed_data.get('question'),
                            self.processed_data.get('answer'),
                            self.processed_data.get('created_at'),
                            self.processed_data.get('category_id'))
        db.session.add(question)
        db.session.flush()
        db.session.commit()

    def __repr__(self):
        return f'{self.processed_data.get("id")}: {self.processed_data.get("question")}'


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

    def __repr__(self):
        return f'{self.question_id}: {self.question_text}'

    def as_json(self):
        return dumps({
            'id': self.id,
            'question_id': self.question_id,
            'question': self.question_text,
            'answer': self.question_answer,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        })


def get_last_question():
    return db.session.query(Question).order_by(Question.id.desc()).first().as_json()


def check_question_exists(id):
    return db.session.execute(db.select(Question).filter_by(question_id=id)).scalar()


def make_request():
    resp = get("https://jservice.io/api/random?count=1").json()[0]
    return make_request() if check_question_exists(resp.get('id')) else resp
