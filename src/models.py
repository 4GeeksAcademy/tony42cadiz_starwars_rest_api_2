from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
	
#1.Definir tablas: Users, People, Planets, Favorites
#Crear relaciones entre tablas
#Aplicar migraciones.

#2.Configurar SQLAlchemy y vincularlo con la app
#Definir rutas y controladores

#3. Endpoints de la API
#3.1.Endpoint para obtener todos los personajes y un personaje por ID
#RUTA [GET] /people
#RUTA [GET] /people/<int:people_id>
#Obtener todos los registros de "people" de la base de datos
#Retornar la lista en formato JSON
#Si no, retornar error 404

#3.2.Endpoint para obtener todos los planetas y un planeta por ID
#RUTA [GET] /planets 
#RUTA [GET] /planets/<int:planet_id>
#Obtener todos los registros de "planets" de la base de datos
#Retornar la lista en formato JSON
#Si no, retornar error 404

#3.3.Endpoint para obtener todos los usuarios y los favoritos de un usuario
#RUTA [GET] /users 
#RUTA [GET] /users/favorites
#Obtener todos los registros de "users" de la base de datos 
#Obtener los registros de "favorites" del usuario actual
#Retornar la lista en formato JSON

#3.4.Endpoint para agregar un planeta y un personaje a favoritos
#RUTA [POST] /favorite/planet/<int:planet_id>
#RUTA [POST] /favorite/people/<int:people_id>
#Verificar si el personaje o el planeta existe en la base de datos
#Si existe, agregarlo a la tabla "favorites" del usuario actual

#3.5.Endpoint para eliminar un planeta y un personaje de favoritos
#RUTA [DELETE] /favorite/planet/<int:planet_id>
#RUTA [DELETE] /favorite/people/<int:people_id>
#Verificar si el planeta o el personaje está en la lista de favoritos del usuario actual
#Si existe, eliminarlo de la tabla "favorites"

#4.Probar todos los endpoints con Postman
    