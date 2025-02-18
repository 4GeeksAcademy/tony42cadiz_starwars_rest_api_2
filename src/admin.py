import os
from flask_admin import Admin
from models import db, User, People, Planet, Favorite
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='StarWars Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session, name="Users", endpoint="admin_users"))
    admin.add_view(ModelView(People, db.session, name="People", endpoint="admin_people"))
    admin.add_view(ModelView(Planet, db.session, name="Planets", endpoint="admin_planets"))
    admin.add_view(ModelView(Favorite, db.session, name="Favorites", endpoint="admin_favorites"))

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
