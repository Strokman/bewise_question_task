from questions import db
from datetime import datetime
from json import dumps


class JServiceApiQuestion:
    """
    Класс предназначен для обработки ответа от
    API jrevice и передачи данных в базу, используя класс Question
    """

    REQUIRED_COLUMNS: tuple[str] = ('id', 'question', 'answer', 'created_at', 'category_id')
    TIME_FORMAT: str = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(self, resp: dict[str, str | int | dict]) -> None:
        """
        При инициализации класс принимает словарь,
        полученный из ответа API jserviсe
        :param resp: dict
        """
        self.data: dict[str, str | int | dict] = resp
        self.processed_data: dict[str, str | int | datetime] = self.extract_needed_data()

    def extract_needed_data(self) -> dict[str, str | int | datetime]:
        """
        Метод выделяет словаря, полученного из json-строки
        ответа API, необходимые для передачи в базу данных.
        Названия необходимых для базы данных колонок
        хранятся в константе-поле класса REQUIRED_COLUMNS.
        Поле created_at (время создания вопроса) конвертируется в
        формат datetime втроенного класса Python (шаблон форматирования
        сохранен в поле класса TIME_FORMAT). Возвращает данные в формате
        словаря.
        :return: dict
        """
        temp_dict: dict[str, str | int | datetime] = dict()
        for key, value in self.data.items():
            if key in self.REQUIRED_COLUMNS:
                temp_dict.setdefault(key, value)
        temp_dict['created_at'] = datetime.strptime(temp_dict['created_at'].replace('Z', '').replace('T', ' '),
                                                    self.TIME_FORMAT)
        return temp_dict

    def commit_to_db(self) -> None:
        """
        Метод создает экземпляр класса Question
        и транслирует его в базу данных, используя
        методы SQLAlchemy
        :return: None
        """
        question: Question = Question(self.processed_data.get('id'),
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
    """
    Класс наследуется от модели SQLAlchemy и содержит поля,
    которые затем будут транслироваться в базу данных,
    в таблицу __tablename__
    """
    __tablename__ = 'questions'

    id: int = db.Column(db.Integer(), nullable=False, primary_key=True)
    question_id: int = db.Column(db.Integer(), nullable=False, unique=True)
    question_text: str = db.Column(db.String(1000), nullable=False)
    question_answer: str = db.Column(db.String(1000), nullable=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False)
    category_id: int = db.Column(db.Integer(), nullable=False)

    def __init__(self, question_id: int,
                 question_text: str,
                 question_answer: str,
                 created_at: datetime,
                 category_id: int) -> None:
        self.question_id = question_id
        self.question_text = question_text
        self.question_answer = question_answer
        self.created_at = created_at
        self.category_id = category_id

    def __repr__(self) -> str:
        return f'{self.question_id}: {self.question_text}'

    def as_json(self) -> str:
        """
        Метод возвращает данные класса в виде json-строки
        :return: str
        """
        return dumps({
            'question_id': self.question_id,
            'question': self.question_text,
            'answer': self.question_answer,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime(JServiceApiQuestion.TIME_FORMAT)
        })
