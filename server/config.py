import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgres://crmagent:MAaMr6M3OG@127.0.0.1/p2p_shop"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
