from server import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password_hash = db.Column(db.String)
    phone = db.Column(db.String)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deleted_at = db.Column(db.DateTime, default=None)
    bought_at = db.Column(db.DateTime, default=None)

    user = db.relationship('User')


class Commentary(db.Model):
    __tablename__ = 'commentaries'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    product = db.relationship('Product')
    user = db.relationship('User')


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    product = db.relationship('Product')
    user = db.relationship('User')


class Authorization(db.Model):
    __tablename__ = 'authorizations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    auth_token = db.Column(db.String)

    user = db.relationship('User')


class Image(db.Model):
    __tablename__ = 'images'
    _model_type = 'image'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    hash = db.Column(db.String(255))
    is_original = db.Column(db.Boolean)


