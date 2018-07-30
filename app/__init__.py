from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(app.instance_path, 'booking.db'),
    )


db = SQLAlchemy(app)

with app.app_context():
    from .models import *
migrate = Migrate(app, db)

from . import import_csv
import_csv.init_app(app)

from .models import Booking, Aplikasi
class BookingAdmin(ModelView):
    column_display_pk = True
    column_searchable_list = ['no_ref']
    column_filters = [Aplikasi.name]
    form_choices = {
        'status': [('paid','paid'), ('pending', 'pending')]
    }
    form_excluded_columns = ['date_created']
class ModelAdmin(ModelView):
    column_display_pk = True

admin = Admin(app, name='Online Booking', template_mode='bootstrap3')
admin.add_view(ModelAdmin(Aplikasi, db.session))
admin.add_view(BookingAdmin(Booking, db.session))


if __name__ == '__main__':
    app.run()