from server import app
from flask import request, jsonify, json, make_response, abort, send_file
from .controllers import BaseController, ImagesController, AuthorizationController, UserController, ProductController,\
    CommentaryController


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,X-Auth-Token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    response.headers.add('Access-Control-Expose-Headers', 'X-Auth-Token')
    return response


def accessed_url(path):
    accessed_url = ['images', 'commentaries', 'products', 'registration', 'auth']
    for url in accessed_url:
        if url in path:
            return True
    return False


@app.before_request
def before_request():
    if not (request.headers.environ.get('REQUEST_METHOD') == 'OPTIONS' or accessed_url(request.path)):
        token = request.headers.get('X-Auth-Token')
        print(request.headers)
        is_auth = AuthorizationController.check_auth(token)
        if not is_auth:
            return abort(401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.route('/<entity>/?', methods=['GET'])
@app.route('/<entity>', methods=['GET'])
@app.route('/<entity>/', methods=['GET'])
@app.route('/<entity>/<entity_id>/?', methods=['GET'])
@app.route('/<entity>/<entity_id>/', methods=['GET'])
@app.route('/<entity>/<entity_id>', methods=['GET'])
def get_entities(entity: str, entity_id: int = None):
    result = BaseController.base_get(entity, entity_id, request.args)
    if result:
        return make_response(jsonify(result))
    else:
        return abort(404)


@app.route('/<entity>/<entity_id>/', methods=['DELETE'])
@app.route('/<entity>/<entity_id>', methods=['DELETE'])
def delete_entity(entity: str, entity_id: int):
    result = BaseController.base_delete(entity, entity_id)
    if result:
        return make_response(jsonify(result))
    return abort(404)
    pass


@app.route('/products/<entity_id>', methods=['DELETE'])
def delete_product(entity_id: int):
    result = ProductController.delete(entity_id)
    if result:
        return make_response(jsonify(result))
    return abort(404)
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
    data = json.loads(request.data.decode('utf-8'))
    auth_result = AuthorizationController.authorize(data)
    if auth_result:
        return make_response(jsonify(auth_result))
    return abort(404)


@app.route('/registration', methods=['POST'])
def registration():
    data = json.loads(request.data.decode('utf-8'))
    user = UserController.create_user(data)
    if user:
        return make_response(jsonify(user))
    return abort(404)


@app.route('/favorites', methods=['GET'])
def get_favorites():
    token = request.headers.get('X-Auth-Token')
    view = ProductController.get_favourite_product(token)
    if view:
        return make_response(jsonify(view))
    return abort(404)


@app.route('/user-products', methods=['GET'])
def user_product():
    token = request.headers.get('X-Auth-Token')
    view = ProductController.get_user_product(token)
    if view:
        return make_response(jsonify(view))
    return abort(404)


@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    view = ProductController.create_product(request)
    return make_response(jsonify(view))
