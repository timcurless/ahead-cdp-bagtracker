from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

from views.index import index
from views.api import api

app.register_blueprint(index)
app.register_blueprint(api)

with app.app_context():
    db.drop_all()
    db.create_all()
