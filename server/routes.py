from server import app
from flask import request, jsonify, json, make_response, abort, send_file
from .controllers import BaseController, ImagesController, AuthorizationController, UserController


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response


@app.before_request
def before_request():
    token = request.headers.get('authToken')
    is_auth = AuthorizationController.check_auth(token)
    if not is_auth:
        return abort(401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.route('/<entity>', methods=['GET'])
@app.route('/<entity>/', methods=['GET'])
@app.route('/<entity>/<entity_id>', methods=['GET'])
def get_entities(entity: str, entity_id: int = None):
    result = BaseController.base_get(entity, entity_id, request.args)
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


@app.route('/images/<hash>', methods=['GET'])
def get_page_image(hash):
    image_path = ImagesController.get_images(hash)
    if image_path:
        return send_file(image_path)
    return abort(404)


@app.route('/authorize', methods=['POST'])
def authorize_user():
    data = request.data
    auth_result = AuthorizationController.authorize(data)
    if auth_result:
        return make_response(auth_result)
    return abort(404)

