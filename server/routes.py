from server import app
from flask import request, jsonify, json, make_response, abort
from server import db
from .models import *
from datetime import datetime


def serialize(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.route('api/v1/users/<id:int>', methods=['GET'])
def get_users(id:int = -1):
    session = db.session()
    result = None
    if id != -1:
        result = session.query(User).filter(User.id == id).one_or_none()
    else:
        result = session.query(User).all()

    pass


@app.route('')
def get_products_by_user_id():
    pass


@app.route('api/v1/auth', methods=['POST'])
def authorization():

    pass


@app.route('api/v1/registration', methods=['POST'])
def registration():
    pass


