from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_PATH, SQLALCHEMY_TRACK_MODIFICATIONS
from util import Gender


db = SQLAlchemy()

"""
rollback_db()
   rollback database
"""
def rollback_db():
    db.session.rollback()


"""
close_db()
   rollback database
"""
def close_db():
    db.session.close()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)


"""
Movie

"""
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(500), nullable=False)
    release_date = Column(DateTime, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
    format()
        representation of the Movie model
    '''

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    '''
    insert()
        inserts a new movie into a database
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new movie into a database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new movie into a database
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'<Movie {self.id} {self.title} {self.release_date}>'


# Actors with attributes name, age and gende


"""
Actor

"""
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    format()
        representation of the Actor model
    '''

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': Gender(self.gender).name,
        }

    '''
    insert()
        inserts a new actor into a database
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new actor into a database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new actor into a database
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'<Actor {self.id} {self.name} {self.age} {Gender(self.gender).name}>'