from server import db


class User:
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    phone = db.Column(db.String)


class Product:
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Double)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')


class Commentary:
    __tablename__ = 'commentaries'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    product = db.relationship('Product')
    user = db.relationship('User')


class Favorite:
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    product = db.relationship('Product')
    user = db.relationship('User')