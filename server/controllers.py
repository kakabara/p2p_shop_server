import json
from .models import *
from server import db
import hashlib
from sqlalchemy import and_
from werkzeug.utils import secure_filename
import os
import hashlib
from .views import ResponseView


def get_dict_table_name_to_class():
    all_classes = set()
    work = [db.Model]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in all_classes:
                all_classes.add(child)
                work.append(child)

    return {klass.__tablename__: klass for klass in all_classes if getattr(klass, '__tablename__')}


table_name_class = get_dict_table_name_to_class()


class BaseController:
    @staticmethod
    def apply_filtered(entity_class, query, filters: dict):
        for filter_key in filters:
            value = filters[filter_key]
            column = getattr(entity_class, filter_key, None)
            filt = getattr(column, '__eq__')(value)
            query = query.filter(filt)
        return query



    @staticmethod
    def create_entity(entity_class, fields: dict):
        entity = entity_class()
        for field in fields:
            setattr(entity, field, fields[field])
        print(1)
        return entity

    @staticmethod
    def update_entity(entity, fields: dict):
        for field in fields:
            setattr(entity, field, fields[field])
        print(1)
        return entity

    @staticmethod
    def base_get(entity: str, entity_id: int = None, filters: dict = dict()):
        entity_class = table_name_class.get(entity)
        #
        if not entity_class:
            return None
        if entity_id:
            result = entity_class.query.filter(entity_class.id == entity_id).one_or_none()
        else:
            query = entity_class.query
            query = BaseController.apply_filtered(entity_class, query, filters)
            result = query.all()
        view = ResponseView.get_view(result)
        return view

    @staticmethod
    def base_post(entity: str, data):
        entity_class = table_name_class.get(entity)

        if not entity_class:
            return None
        data = json.loads(data.decode('utf-8'))
        result = BaseController.create_entity(entity_class, data)
        db.session.add(result)
        db.session.commit()
        view = ResponseView.get_view(result)
        return view

    @staticmethod
    def base_update(entity: str, entity_id: int, data):
        entity_class = table_name_class.get(entity)
        if not entity_class:
            return None
        entity = entity_class.query.filter(entity_class.id == entity_id).one_or_none()
        if not entity:
            return None
        data = json.loads(data.decode('utf-8'))
        result = BaseController.update_entity(entity, data)
        db.session.add(result)
        db.session.commit()
        view = ResponseView.get_view(result)(result)
        return view

    @staticmethod
    def base_delete(entity: str, entity_id: int):
        entity_class = table_name_class.get(entity)

        if not entity_class:
            return None
        entity = entity_class.query.filter(entity_class.id == entity_id).one_or_none()
        db.session.delete(entity)
        db.session.commit()
        return {"status": "done"}


class ImagesController:
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ImagesController.ALLOWED_EXTENSIONS

    @staticmethod
    def get_images(image_hash):
        image = Image.query.filter(Image.hash == image_hash).one_or_none()
        if image:
            return image.path
        return None

    @staticmethod
    def save_image(request):
        directory_to_save = '/data/p2p-data/images'
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return {'error': 'bad request'}
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return {'error': 'bad request'}
            if file and ImagesController.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_full_path = os.path.join(directory_to_save, filename)
                file.save(file_full_path)

                hash_file = Hasher.get_hash(file_full_path)

                image = Image(path=file_full_path, hash=hash_file)
                db.session.add(image)
                db.session.commit()
                return image
        return {'error': 'bad request'}


class UserController:
    @staticmethod
    def create_user(data):
        login = data.get('login')
        password = data.get('password')
        phone = data.get('phone')

        if login and password and phone:
            exist_user = User.query.filter(User.login == login).one_or_none()
            if exist_user:
                return {'error': 'this login has been used'}
            else:
                password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()

                new_user = User(login=login, password_hash=password_hash, phone=phone)
                db.session.add(new_user)
                db.session.commit()

                return AuthorizationController.authorize({'login': login, 'password': password})
        return None


class AuthorizationController:
    @staticmethod
    def authorize(data):
        login = data.get('login')
        password = data.get('password')
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()

        is_user = User.query.filter(and_(User.login == login, User.password_hash == password_hash)).one_or_none()

        if is_user:
            token = hashlib.sha1((login + password_hash).encode('utf-8')).hexdigest()
            if not AuthorizationController.check_auth(token):
                new_auth = Authorization(user=is_user, auth_token=token)
                db.session.add(new_auth)
                db.session.commit()
            return {'authToken': token, 'user_id': is_user.id}
        return None

    @staticmethod
    def check_auth(token):
        auth = Authorization.query.filter(Authorization.auth_token == token).one_or_none()
        if auth:
            return token
        return None

    @staticmethod
    def get_user_by_token(token):
        auth = Authorization.query.filter(Authorization.auth_token == token).one_or_none()
        if auth:
            return auth.user


class CommentaryController:
    @staticmethod
    def get_commentary():
        commentaries = Commentary.query.limit(20).all()
        if commentaries:
            view = ResponseView.get_view(commentaries)
            return view
        return 404
        pass


class ProductController:
    @staticmethod
    def get_favourite_product(token):
        user = AuthorizationController.get_user_by_token(token)
        favorite_products = BaseController.base_get('favorites', None, {'user_id': user.id})
        products = []
        for fav in favorite_products:
            products.append(fav.get('product'))
        if products:
            return products
        return None

    @staticmethod
    def get_user_product(token):
        user = AuthorizationController.get_user_by_token(token)
        products = BaseController.base_get('products', None, {'user_id': user.id})
        if products:
            return products
        return None

    @staticmethod
    def create_product(request):
        image = ImagesController.save_image(request)
        if isinstance(image, dict):
            return image

        user = AuthorizationController.get_user_by_token(request.headers.get('X-Auth-Token'))
        data = json.loads(request.form.get('data'))
        if user:
            product = Product(name=data.get('name'), description=data.get('description'), user_id=user.id,
                              price=data.get('price'), image=image)

            db.session.add(product)
            db.session.commit()

            return ResponseView.get_view(product)
        return {'error': 'bad_request'}

class Hasher:
    @staticmethod
    def get_hash(file):
        """
        Get hash from file

        :param file: str; Path to file
        :return: str
        """

        blocksize = 65536
        hasher = hashlib.md5()

        with open(file, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)

        hasher.update(str(datetime.now()).encode('utf-8'))

        return hasher.hexdigest()