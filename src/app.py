"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People, Planet, FavoritePlanets,FavoritePeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def users():
    all_users=User.query.all()
    all_users_serialize=[user.serialize() for user in all_users]

    return jsonify(all_users_serialize), 200


@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people_seralized= []
    for person in all_people:
        all_people_seralized.append(person.serialize())
    return jsonify({'msg':'get people ok', 'data': all_people_seralized})

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    all_planets_seralized= []
    for planets in all_planets:
        all_planets_seralized.append(planets.serialize())
    return jsonify({'msg':'get people ok', 'data': all_planets_seralized})


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({'msg': f"El personaje con id {people_id} no existe"}), 400
    return jsonify({'data':person.serialize()})

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_single_planet(planets_id):
    planet = Planet.query.get(planets_id)
    if planet is None:
        return jsonify({'msg': f"El planeta con id {planets_id} no existe"}), 400
    return jsonify({'data':planet.serialize()})

@app.route('/user/<int:user_id>/favorites' , methods=['GET'])
def get_favorites_by_user(user_id):
    favoritesplanets = FavoritePlanets.query.filter_by(user_id=user_id).all()
    favorite_planets_serialized = [fav.serialize() for fav in favoritesplanets ]
    favoritepeople = FavoritePeople.query.filter_by(user_id=user_id).all()
    favorite_people_serialized = [fav.serialize() for fav in favoritepeople ]
    
    return jsonify({'favorite_planets': favorite_planets_serialized,"favorite_people": favorite_people_serialized})


@app.route('/people', methods=['POST'])
def add_person():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debes enviar Name y Age en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'El campo name es obligatorio'}), 400
    if 'age' not in body:
        return jsonify({'msg': 'El campo age es obligatorio'}), 400
    

    new_person=People()
    new_person.name= body['name']
    new_person.age= body ['age']
    db.session.add(new_person)
    db.session.commit()
    return jsonify ({'msg':'new person added', 'data': new_person.serialize()})

@app.route('/user/<int:user_id>/favorites_planets/<int:planet_id>' , methods=['POST'])
def add_planet_favorites(user_id,planet_id):
    exist = FavoritePlanets.query.filter_by(user_id=user_id,planet_id=planet_id).first()
    if exist:
        return jsonify("El Planeta ya Existia En los Favoritos"), 400 
    new_favorite=FavoritePlanets(user_id=user_id,planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({'msg':'new favorite added', 'data': new_favorite.serialize()})

@app.route('/user/<int:user_id>/favorites_people/<int:people_id>' , methods=['POST'])
def add_people_favorites(user_id,people_id):
    exist = FavoritePeople.query.filter_by(user_id=user_id,people_id=people_id).first()
    if exist:
        return jsonify("El Personaje ya existia en los favoritos"), 400 
    new_favorite=FavoritePeople(user_id=user_id,people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify ({'msg':'new favorite people', 'data': new_favorite.serialize()})

@app.route('/user/<int:user_id>/favorites_planets/<int:planet_id>' , methods=['DELETE'])
def remove_planet_favorite(user_id, planet_id):
    exist = FavoritePlanets.query.filter_by(user_id=user_id,planet_id=planet_id).first()
    if not exist: 
        return jsonify ("favorito No Encontrado"), 400
    db.session.delete(exist)
    db.session.commit()
    return jsonify ("Planet eliminado de Favoritos"), 200 

@app.route('/user/<int:user_id>/favorites_people/<int:people_id>' , methods=['DELETE'])
def remove_people_favorite(user_id, people_id):
    exist = FavoritePeople.query.filter_by(user_id=user_id,people_id=people_id).first()
    if not exist: 
        return jsonify ("favorito No Encontrado"), 400
    db.session.delete(exist)
    db.session.commit()
    return jsonify ("Personaje eliminado de Favoritos"), 200 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


