from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planet_favorites = db.relationship('FavoritePlanets', back_populates='user')
    people_favorites = db.relationship('FavoritePeople', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = 'people'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), unique=True, nullable=False)
    age= db.Column(db.Integer, unique=False, nullable=False)
    home= db.Column(db.String(50), unique=False, nullable=False)
    planet_id= db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship('Planet', back_populates='people')
    favorite_by = db.relationship('FavoritePeople', back_populates='people_favorites')

    def __repr__(self):
        return f'El personaje {self.id} con nombre {self.name}'
    
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "age": self.age,
            "home": self.home
        }

class Planet (db.Model):
    __tablename__= 'planet'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column (db.String(50), unique=True, nullable=False)
    terrain= db.Column (db.String(50), unique=True, nullable=False)
    population= db.Column (db.String (50), unique= True, nullable=False)
    climate= db.Column (db.String (50), unique=True, nullable=False)
    created= db.Column (db.String (50), unique=True, nullable=False)
    people= db.relationship('People', back_populates='planet')
    favorite_by = db.relationship('FavoritePlanets', back_populates='planets_favorites')

    def __repr__(self):    
        return f'Planeta de ID {self.id} con nombre {self.name}'

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "climate": self.climate,
            "created": self.created
        }
    
class FavoritePlanets(db.Model):
        __tablename__='favorite_planets'
        id= db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        user= db.relationship('User', back_populates='planet_favorites')
        planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
        planets_favorites= db.relationship('Planet', back_populates='favorite_by')

        def __repr__(self):
            return f'Al usuario {self.user_id} le gusta planeta {self.planet_id}'

        def serialize(self):
            return{
                'id':self.id,
                'user_id': self.user_id,
                'planet_id': self.planet_id
            }

class FavoritePeople(db.Model):
        __tablename__='favorite_people'
        id= db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        user= db.relationship('User', back_populates='people_favorites')
        people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
        people_favorites= db.relationship('People', back_populates='favorite_by')

        def __repr__(self):
            return f'Al usuario {self.user_id} le gusta el personaje {self.people_id}'

        def serialize(self):
            return{
                'id':self.id,
                'user_id': self.user_id,
                'people_id': self.people_id
            }        
