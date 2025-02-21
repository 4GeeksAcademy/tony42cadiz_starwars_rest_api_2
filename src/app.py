"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de herramientas
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores globales
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar el sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ======================== RUTAS ======================== #

# Obtener todas las personas
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200

# Obtener una persona específica
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    return jsonify(person.serialize()), 200

# Obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

# Obtener un planeta específico
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.serialize()), 200

# Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

# Obtener los favoritos de un usuario específico
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([fav.serialize() for fav in user.favorites]), 200

# Agregar un planeta a favoritos
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get_or_404(user_id)
    planet = Planet.query.get_or_404(planet_id)

    # Verificar si ya está en favoritos
    existing_fav = Favorite.query.filter_by(user_id=user.id, planet_id=planet.id).first()
    if existing_fav:
        return jsonify({'message': 'Este planeta ya está en favoritos'}), 400

    new_fav = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({'message': 'Planeta agregado a favoritos'}), 201

# Agregar una persona a favoritos
@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    user = User.query.get_or_404(user_id)
    person = People.query.get_or_404(people_id)

    # Verificar si ya está en favoritos
    existing_fav = Favorite.query.filter_by(user_id=user.id, people_id=person.id).first()
    if existing_fav:
        return jsonify({'message': 'Este personaje ya está en favoritos'}), 400

    new_fav = Favorite(user_id=user.id, people_id=person.id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({'message': 'Personaje agregado a favoritos'}), 201

# Eliminar un planeta de favoritos
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({'message': 'Planeta no encontrado en favoritos'}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({'message': 'Planeta eliminado de favoritos'}), 200

# Eliminar una persona de favoritos
@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    fav = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({'message': 'Personaje no encontrado en favoritos'}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({'message': 'Personaje eliminado de favoritos'}), 200

# ======================== EJECUCIÓN ======================== #
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
