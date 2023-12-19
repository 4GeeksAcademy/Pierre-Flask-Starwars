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
from models import db, User, People, Planet, Favorites
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

# Add new user 
@app.route('/user', methods=['POST'])
def handle_hello():
    req_body = request.get_json()

    user_email = req_body['email']
    user_password = req_body['password']
    user_is_active = req_body['is_active'] 

    new_user = User(email=user_email, password=user_password, is_active=user_is_active)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({ 'Message': 'Posted new user'}), 200


# Get a list of all the blog post users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = []
    for user in users:
        serialized_users.append(user.serialize())
    
    if len(serialized_users) > 0:
        return jsonify(serialized_users), 200
    
    return jsonify({ 'message': 'No users in db'}), 404

# Get a list of all the people in the database
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people = []
    for person in people:
        serialized_people.append(person.serialize())
    
    if len(serialized_people) > 0:
        return jsonify(serialized_people), 200
    
    return jsonify({ 'message': 'No people in db'}), 404


# Add new person
@app.route('/person', methods=['POST'])
def add_person():
    req_body = request.get_json()

    person_name = req_body['name']
    person_about = req_body['about']

    new_person = People(name = person_name, about = person_about)

    db.session.add(new_person)
    db.session.commit()
    return jsonify({ 'Message': 'Posted new person to db'}), 200
    

# Get single person
@app.route('/person/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = People.query.get(person_id)

    if person:
        return jsonify(person.serialize()), 200
    
    return jsonify({'message': 'Person not found'}), 404


# Get all the favorites that belong to the current user
@app.route('/users/favorite/<int:user_id>')
def get_all_favorites(user_id):
    user = User.query.get(user_id)

    serialize_favorites = []
    for favorite in user.favorites:
        serialize_favorites.append(favorite.serialize())

    if len(serialize_favorites) > 0:
        return jsonify(serialize_favorites), 200
    
    return jsonify({ 'message': "Cannot find favorite"}), 404


# Add Planet 
@app.route('/planets', methods = ['POST'])
def add_planet():
    req_body = request.get_json() 

    planet_name = req_body['name']
    planet_about = req_body['about']

    new_planet = Planet(name = planet_name, about = planet_about)

    db.session.add(new_planet)
    db.session.commit()
    return jsonify({ 'Message': 'Posted new planet to db'}), 200


# Get a list of all the planets in the database
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = []
    for planet in planets:
        serialized_planets.append(planet.serialize())
    
    if len(serialized_planets) > 0:
        return jsonify(serialized_planets), 200
    
    return jsonify({ 'message': 'No people in db'}), 404

# Get one single planet information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet:
        return jsonify(planet), 200
    return jsonify({ "message": "No planet found"}), 404
    
# Add a new favorite planet to the current user with the planet id = planet_id
@app.route('/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  

    current_user = User.query.get(user_id)

    if current_user:
        planet = Planet.query.get(planet_id)

        favorites = Favorites()
        favorites.user = current_user
        favorites.planet = planet

        current_user.favorites.append(favorites)
        db.session.commit()

        return jsonify({ 'Message': 'Added planet to user favorites'}), 200
    
    return jsonify({"Message": "Error Adding planet"}), 404


# Add new favorite people to the current user with the people id = people_id
@app.route("/favorite/people/<int:person_id>", methods=['POST'])
def add_favorite_person(person_id):
    user_id = 3

    current_user = User.query.get(user_id)

    if current_user:
        person = People.query.get(person_id)

        favorites = Favorites()
        favorites.user = current_user
        favorites.person = person

        current_user.favorites.append(favorites)
        db.session.commit()
        return jsonify({ 'Message': 'Added person to user favorites'}), 200
    
    return jsonify({"Message": "Error Adding planet"}), 404



# Delete favorite planet with the id = planet_id
@app.route('/favorite/planet/<int:planet_id>',  methods=['DELETE'])
def delete_planet(planet_id):

    planet = Favorites.query.get(planet_id)

    print ("planet!!!!", planet)

    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({ 'Message': 'Removed planet from DB'}), 200

    return jsonify({ "Message": "Error removing planet from DB"}), 404



#  Delete favorite people with the id = people_id
@app.route('/favorite/people/<int:person_id>',  methods=['DELETE'])
def delete_planet(person_id):

    person = Favorites.query.get(person_id)

    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({ 'Message': 'Removed person from DB'}), 200

    return jsonify({ "Message": "Error removing person from DB"}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


