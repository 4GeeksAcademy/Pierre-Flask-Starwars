from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": self.favorites
            # do not serialize the password, its a security breach
        }

    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favorite_people = db.relationship('People')
    favorite_planet = db.relationship('Planet')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_people": self.favorite_people,
            "favorite_planet": self.favorite_planet,
        }

    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    about = db.Column(db.String(120), unique=True)
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "about": self.about
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    about = db.Column(db.String(120))
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "about": self.about
        }





