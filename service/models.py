from requests import get
from service import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError, PendingRollbackError


class JServiceApiHandler:

    REQUIRED_COLUMNS = ('id', 'question', 'answer', 'created_at', 'category_id')

    def __init__(self, count):
        self.count = count
        self.data = get(f"https://jservice.io/api/random?count={count}")
        self.ready_data = self.extract_needed_data()

    # def json_data(self):
    #     return self.data.json()

    def get_question(self):
        counter = self.count
        for i in range(counter):


    def extract_needed_data(self):
        temp_list = []
        for item in self.data.json():
            question = dict()
            for key, value in item.items():
                if key in self.REQUIRED_COLUMNS:
                    question[key] = value
            question['created_at'] = self.convert_time(question['created_at'].replace('Z', '').replace('T', ' '))
            temp_list.append(question)
        return temp_list


    def commit_to_db(self):
        for item in self.ready_data:
            try:
                question = Question(item['id'], item['question'], item['answer'],
                                    item['created_at'], item['category_id'])
                db.session.add(question)
                db.session.flush()
                db.session.commit()
                print('ok')

            except (IntegrityError, PendingRollbackError):
                print("question exists")
                obj = JServiceApiHandler(1)
                obj.commit_to_db()
                continue
        return "Succesfull", 200



    def convert_time(self, time: str):
        return datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')


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






