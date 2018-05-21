from server import db
from datetime import datetime


class Mixin:
    def _field_relationships(self):
        for rel in db.class_mapper(self.__class__).relationships._data.keys():
            yield rel


class User(db.Model, Mixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password_hash = db.Column(db.String)
    phone = db.Column(db.String)


class Product(db.Model, Mixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deleted_at = db.Column(db.DateTime, default=None)
    bought_at = db.Column(db.DateTime, default=None)

    image_hash = db.Column(db.String(255), db.ForeignKey('images.hash'))
    user = db.relationship('User', primaryjoin='Product.user_id == User.id')
    image = db.relationship('Image')

    bought_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyer = db.relationship('User', primaryjoin='Product.bought_by == User.id')


class Commentary(db.Model, Mixin):
    __tablename__ = 'commentaries'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    product = db.relationship('Product')
    user = db.relationship('User')


class Favorite(db.Model, Mixin):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    product = db.relationship('Product')
    user = db.relationship('User')


class Authorization(db.Model, Mixin):
    __tablename__ = 'authorizations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    auth_token = db.Column(db.String)

    user = db.relationship('User')


class Image(db.Model, Mixin):
    __tablename__ = 'images'
    _model_type = 'image'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    hash = db.Column(db.String(255), unique=True)



