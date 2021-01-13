from app import db


class UserWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    power = db.Column(db.Integer, default=0)
    practice_point = db.Column(db.Integer, default=0)
    appear_count = db.Column(db.Integer, default=0)
    search_count = db.Column(db.Integer, default=0)

    def __init(self, user_id, word_id):
        self.user_id = user_id
        self.word_id = word_id

    def increasePracticePoint(self, practice_point):
        self.practice_point += practice_point

    def increaseAppearCount(self):
        self.appear_count += 1

    def increaseSearchCount(self):
        self.search_count += 1

    def calculatePower(self):
        self.power +=  ( 2 * self.practice_point ) + (self.search_count) + (self.appear_count)


class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     password = db.Column(db.String(120), nullable=False)
     userwords = db.relationship('UserWord', backref='user', lazy=True)



     def __init__(self, name, password):
        self.username = name
        self.password = password


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=True, nullable=False)
    userwords = db.relationship('UserWord', backref='word', lazy=True)
    definitions = db.relationship('Definition', backref='word', lazy=True)

    def __init__(self, word):
        self.word = word




class Definition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    definition = db.Column(db.String(500), nullable=False)

    def __init__(self,word_id,definition):
        self.word_id = word_id
        self.definition = definition

