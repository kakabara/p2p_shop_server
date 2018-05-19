from flask import Flask
from server.config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


UPLOAD_FOLDER = '/path/to/the/uploads'

app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from server import routes, models
