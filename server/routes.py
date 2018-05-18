from server import app
from flask import request, jsonify, json, make_response, abort

from .controllers import BaseController


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.route('/<entity>/', methods=['GET'])
@app.route('/<entity>/<entity_id>', methods=['GET'])
def get_entities(entity: str, entity_id: int = None):
    result = BaseController.base_get(entity, entity_id)
    if result:
        return make_response(jsonify(result))
    else:
        return abort(404)


@app.route('/<entity>/<entity_id>', methods=['DELETE'])
def delete_entity(entity: str, entity_id: int):
    result = BaseController.base_delete(entity, entity_id)
    return make_response(jsonify(result))
    pass


@app.route('/<entity>', methods=['POST'])
@app.route('/<entity>/', methods=['POST'])
def create_entity(entity: str):
    result = BaseController.base_post(entity, request.data)
    return make_response(jsonify(result))
    pass


@app.route('/<entity>/<entity_id>', methods=['PATCH'])
def update_entity(entity: str, entity_id):
    result = BaseController.base_update(entity, entity_id, request.data)
    return make_response(jsonify(result))
