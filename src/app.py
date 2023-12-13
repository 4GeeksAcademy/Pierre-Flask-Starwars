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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = []
    for user in users:
        serialized_users.append(user.serialize())
    
    if len(serialized_users) > 0:
        return jsonify(serialized_users), 200
    
    return jsonify({ 'message': 'No users'}), 404

# Get all people
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people = []
    for person in people:
        serialized_people.append(person.serialize())
    
    if len(serialized_people) > 0:
        return jsonify(serialized_people), 200
    
    return jsonify({ 'message': 'No people'}), 404
    

# Get single person
@app.route('/people/<int:people_id>')
def get_single_person(person_id):
    person = People.query.get(person_id = person_id)

    if person:
        return jsonify(person.serialize()), 200
    
    return jsonify({'message': 'Person not found'}), 404

# Get all favorites
@app.route('/users/favorite')
def get_all_favorites(user_id):
    user = User.query.get(user_id = user_id)

    serialize_favorites = []
    for favorite in user.favorites:
        serialize_favorites.append(favorite.serialize())

    if len(serialize_favorites) > 0:
        return jsonify(serialize_favorites)
    
    return jsonify({ 'message': "Cannot find favorite"})


# Get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify(planets)

# Get Single Planet
@app.route('/planets/<int:planet_id>')
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet:
        return jsonify(planet)
    return jsonify({ "message": "No planet found"}), 200
    
# Favorite planet routes
@app.route('/favorite/planet/<int:planet_id>')
def favorite_planet_routes(planet_id):
    body = request.get_json()
    planet = Favorites.query.filter_by(body, planet_id)
    if request.method == 'DELETE':
        Favorites.delete(planet)
        db.session.commit()
    if request.method == 'POST':
        Favorites.query.add(body)
        db.session.commit()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


