from requests import get
from service import db
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, PendingRollbackError


class JServiceApiQuestion:

    REQUIRED_COLUMNS = ('id', 'question', 'answer', 'created_at', 'category_id')
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(self, count):
        self.data = get(f"https://jservice.io/api/random?count={count}")
        self.processed_data = self.extract_needed_data()
        # self.exists = self.check_db(self.processed_data.get('id'))


    def extract_needed_data(self):
        questions_list = []
        for item in self.data.json():
            print(item)
            d = {}
            for key, value in item.items():
                print(key, value)
                if key in self.REQUIRED_COLUMNS:
                    d.setdefault(key, value)
            d['created_at'] = self.convert_time(d['created_at'].replace('Z', '').replace('T', ' '))
            questions_list.append(d)
        return questions_list

    # def check_db(self, id):
    #     if db.session.execute(db.select(Question).filter_by(question_id=id)).scalar():
    #         print(db.session.execute(db.select(Question).filter_by(question_id=id)).first())
    #         print('exists')
    #         return True
    #     return False

    def commit_to_db(self):
        if not self.exists:
        # try:
            question = Question(self.processed_data.get('id'), self.processed_data.get('question'),
                                self.processed_data.get('answer'), self.processed_data.get('created_at'),
                                self.processed_data.get('category_id'))
            db.session.add(question)
            db.session.flush()
            db.session.commit()
            print('ok')
        # except (IntegrityError, PendingRollbackError):
        #     return 'Forbidden', 403
            return "Successful", 200

    def convert_time(self, time: str):
        return datetime.strptime(time, self.TIME_FORMAT)



#
#
# def get_question(count):
#     for i in range(count):
#         a = JServiceApiQuestion()
#         if check_db(a.processed_data.get('id')):
#             a = JServiceApiQuestion()
#             a.commit_to_db()
#         else:
#             a.commit_to_db()


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
